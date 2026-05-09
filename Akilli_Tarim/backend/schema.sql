-- ============================================================
--  Akıllı Tarım Yönetim Sistemi
--  Veritabanı Şeması – schema.sql
--  PostgreSQL 15+
--  Hazırlayan : Binnur Aslan
--  Güncelleme : Hafta 3 – ml_sonuclari tablosu eklendi
--  Son Güncelleme: 2026-05-03
-- ============================================================


-- ============================================================
-- 1. KULLANICILAR
-- ============================================================
CREATE TABLE kullanicilar (
    id             SERIAL        PRIMARY KEY,
    kullanici_adi  VARCHAR(50)   UNIQUE NOT NULL,
    sifre_hash     VARCHAR(255)  NOT NULL,
    email          VARCHAR(200)  UNIQUE NOT NULL,
    ad_soyad       VARCHAR(150)  NOT NULL,
    rol            VARCHAR(20)   DEFAULT 'ciftci',
    kayit_tarihi   TIMESTAMPTZ   DEFAULT NOW()
);

-- ============================================================
-- 2. TARLALAR
-- ============================================================
CREATE TABLE tarlalar (
    id           SERIAL         PRIMARY KEY,
    kullanici_id INTEGER        REFERENCES kullanicilar(id) ON DELETE CASCADE,
    ad           VARCHAR(100)   NOT NULL,
    bitki_turu   VARCHAR(100),
    konum        POINT,
    toprak_tipi  VARCHAR(50),
    alan_m2      DECIMAL(10,2)
);

-- ============================================================
-- 3. SENSORLER
-- ============================================================
CREATE TABLE sensorler (
    id        SERIAL        PRIMARY KEY,
    tarla_id  INTEGER       REFERENCES tarlalar(id) ON DELETE CASCADE,
    ad        VARCHAR(100)  NOT NULL,
    tip       VARCHAR(50)   NOT NULL,
    konum     POINT,
    aktif_mi  BOOLEAN       DEFAULT TRUE
);

-- ============================================================
-- 4. OLCUMLER  (en büyük tablo — ~5.3M satır/yıl)
-- ============================================================
CREATE TABLE olcumler (
    id            BIGSERIAL      PRIMARY KEY,
    sensor_id     INTEGER        REFERENCES sensorler(id),
    tarla_id      INTEGER        REFERENCES tarlalar(id),
    olcum_zamani  TIMESTAMPTZ    NOT NULL,
    deger         DECIMAL(10,4)  NOT NULL,
    birim         VARCHAR(20),
    ham_veri      JSONB
);

-- ============================================================
-- 5. HAVA_DURUMU
-- ============================================================
CREATE TABLE hava_durumu (
    id            SERIAL         PRIMARY KEY,
    tarla_id      INTEGER        REFERENCES tarlalar(id),
    olcum_zamani  TIMESTAMPTZ    NOT NULL,
    sicaklik      DECIMAL(5,2),
    nem           DECIMAL(5,2),
    yagis_mm      DECIMAL(6,2),
    ruzgar_hizi   DECIMAL(5,2),
    veri_kaynagi  VARCHAR(50)
);

-- ============================================================
-- 6. TAVSIYELER
-- ============================================================
CREATE TABLE tavsiyeler (
    id                      SERIAL        PRIMARY KEY,
    tarla_id                INTEGER       REFERENCES tarlalar(id),
    olusturulma_zamani      TIMESTAMPTZ   DEFAULT NOW(),
    tavsiye_tipi            VARCHAR(50),
    aciliyet                VARCHAR(20),
    durum                   VARCHAR(20)   DEFAULT 'bekliyor',
    uygulayan_kullanici_id  INTEGER       REFERENCES kullanicilar(id)
);

-- ============================================================
-- 7. ML_SONUCLARI  ★ Hafta 3 — TensorFlow model çıktıları
-- ============================================================
CREATE TABLE ml_sonuclari (
    id               BIGSERIAL      PRIMARY KEY,
    tarla_id         INTEGER        REFERENCES tarlalar(id),
    sensor_id        INTEGER        REFERENCES sensorler(id),
    model_adi        VARCHAR(100)   NOT NULL,
    model_versiyonu  VARCHAR(20),
    tahmin_zamani    TIMESTAMPTZ    DEFAULT NOW(),
    girdi_verisi     JSONB,
    tahmin_sonucu    VARCHAR(100),
    guven_skoru      DECIMAL(5,4),
    detay            JSONB
);

-- ============================================================
-- INDEKSLER
-- ============================================================
CREATE INDEX idx_olcumler_zaman    ON olcumler(olcum_zamani DESC);
CREATE INDEX idx_olcumler_sensor   ON olcumler(sensor_id);
CREATE INDEX idx_olcumler_tarla    ON olcumler(tarla_id);
CREATE INDEX idx_olcumler_bilesen  ON olcumler(sensor_id, olcum_zamani DESC);
CREATE INDEX idx_hava_tarla_zaman  ON hava_durumu(tarla_id, olcum_zamani DESC);
CREATE INDEX idx_tavsiye_durum     ON tavsiyeler(durum);
CREATE INDEX idx_ml_model_zaman    ON ml_sonuclari(model_adi, tahmin_zamani DESC);
CREATE INDEX idx_ml_tarla          ON ml_sonuclari(tarla_id);
