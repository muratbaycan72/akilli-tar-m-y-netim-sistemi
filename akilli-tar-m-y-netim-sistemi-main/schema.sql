-- schema.sql
-- Akıllı Tarım Yönetim Sistemi Veritabanı Şeması

CREATE TABLE IF NOT EXISTS Kullanicilar (
    Kullanici_ID SERIAL PRIMARY KEY,
    Ad VARCHAR(100) NOT NULL,
    Soyad VARCHAR(100) NOT NULL,
    Rol VARCHAR(50) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    Sifre_Hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ciftciler (
    Ciftci_ID SERIAL PRIMARY KEY,
    Ad VARCHAR(100) NOT NULL,
    Soyad VARCHAR(100) NOT NULL,
    Telefon VARCHAR(20),
    Email VARCHAR(150) UNIQUE,
    Adres TEXT
);

CREATE TABLE IF NOT EXISTS Tarlalar (
    Tarla_ID SERIAL PRIMARY KEY,
    Ciftci_ID INT NOT NULL,
    Konum VARCHAR(255),
    Alan NUMERIC(10, 2), -- Hektar veya dönüm
    Urun_Turu VARCHAR(100),
    FOREIGN KEY (Ciftci_ID) REFERENCES Ciftciler(Ciftci_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Urunler (
    Urun_ID SERIAL PRIMARY KEY,
    Tarla_ID INT NOT NULL,
    Urun_Adi VARCHAR(100) NOT NULL,
    Ekim_Tarihi DATE,
    Hasat_Tarihi DATE,
    Miktar NUMERIC(15, 2),
    FOREIGN KEY (Tarla_ID) REFERENCES Tarlalar(Tarla_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Sensorler (
    Sensor_ID SERIAL PRIMARY KEY,
    Tarla_ID INT NOT NULL,
    Sensor_Turu VARCHAR(100) NOT NULL,
    Kurulum_Tarihi DATE,
    Durum VARCHAR(50) DEFAULT 'Aktif',
    FOREIGN KEY (Tarla_ID) REFERENCES Tarlalar(Tarla_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Olcumler (
    Olcum_ID SERIAL PRIMARY KEY,
    Sensor_ID INT NOT NULL,
    Tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Deger NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (Sensor_ID) REFERENCES Sensorler(Sensor_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Sulama (
    Sulama_ID SERIAL PRIMARY KEY,
    Tarla_ID INT NOT NULL,
    Tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Sure INT, -- Dakika cinsinden
    Su_Miktari NUMERIC(10, 2), -- Litre veya m3
    FOREIGN KEY (Tarla_ID) REFERENCES Tarlalar(Tarla_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Gubreleme (
    Gubreleme_ID SERIAL PRIMARY KEY,
    Tarla_ID INT NOT NULL,
    Tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Gubre_Turu VARCHAR(100),
    Miktar NUMERIC(10, 2), -- kg veya litre
    FOREIGN KEY (Tarla_ID) REFERENCES Tarlalar(Tarla_ID) ON DELETE CASCADE
);

-- İndeks Tanımlamaları (Sorgu performansını artırmak için ForeignKey alanlarına Index)
CREATE INDEX IF NOT EXISTS idx_tarlalar_ciftci_id ON Tarlalar(Ciftci_ID);
CREATE INDEX IF NOT EXISTS idx_urunler_tarla_id ON Urunler(Tarla_ID);
CREATE INDEX IF NOT EXISTS idx_sensorler_tarla_id ON Sensorler(Tarla_ID);
CREATE INDEX IF NOT EXISTS idx_olcumler_sensor_id ON Olcumler(Sensor_ID);
CREATE INDEX IF NOT EXISTS idx_sulama_tarla_id ON Sulama(Tarla_ID);
CREATE INDEX IF NOT EXISTS idx_gubreleme_tarla_id ON Gubreleme(Tarla_ID);
