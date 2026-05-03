-- ============================================================
--  Akıllı Tarım Yönetim Sistemi
--  Veritabanı Şeması – schema.sql
--  PostgreSQL 15+
--  Hazırlayan : Binnur Aslan
--  Son Güncelleme: 2026-05-03
-- ============================================================


-- ============================================================
-- 1. KULLANICILAR
--    Sisteme giriş yapan çiftçi ve yönetici hesapları
-- ============================================================
CREATE TABLE kullanicilar (
    id             SERIAL        PRIMARY KEY,
    kullanici_adi  VARCHAR(50)   UNIQUE NOT NULL,
    sifre_hash     VARCHAR(255)  NOT NULL,          -- bcrypt (maliyet: 12)
    email          VARCHAR(200)  UNIQUE NOT NULL,
    ad_soyad       VARCHAR(150)  NOT NULL,
    rol            VARCHAR(20)   DEFAULT 'ciftci',  -- ciftci | yonetici | teknisyen
    kayit_tarihi   TIMESTAMPTZ   DEFAULT NOW()
);


-- ============================================================
-- 2. TARLALAR
--    Kullanıcılara ait arazi kayıtları
-- ============================================================
CREATE TABLE tarlalar (
    id           SERIAL         PRIMARY KEY,
    kullanici_id INTEGER        REFERENCES kullanicilar(id) ON DELETE CASCADE,
    ad           VARCHAR(100)   NOT NULL,
    bitki_turu   VARCHAR(100),
    konum        POINT,                             -- GPS (enlem, boylam)
    toprak_tipi  VARCHAR(50),                       -- killi | kumlu | tinli
    alan_m2      DECIMAL(10,2)
);


-- ============================================================
-- 3. SENSORLER
--    Tarlalara yerleştirilen IoT cihazları
-- ============================================================
CREATE TABLE sensorler (
    id        SERIAL        PRIMARY KEY,
    tarla_id  INTEGER       REFERENCES tarlalar(id) ON DELETE CASCADE,
    ad        VARCHAR(100)  NOT NULL,
    tip       VARCHAR(50)   NOT NULL,   -- toprak_nemi | sicaklik | isik | ph
    konum     POINT,
    aktif_mi  BOOLEAN       DEFAULT TRUE
);


-- ============================================================
-- 4. OLCUMLER  ★ En kritik tablo
--    5 dk'da bir gelen ham sensör verileri
--    Tahmini hacim: ~5.3 milyon satır/yıl (50 sensör)
-- ============================================================
CREATE TABLE olcumler (
    id            BIGSERIAL      PRIMARY KEY,
    sensor_id     INTEGER        REFERENCES sensorler(id),
    tarla_id      INTEGER        REFERENCES tarlalar(id),
    olcum_zamani  TIMESTAMPTZ    NOT NULL,
    deger         DECIMAL(10,4)  NOT NULL,
    birim         VARCHAR(20),   -- % | °C | lux | pH
    ham_veri      JSONB          -- batarya, sinyal gücü vb. ek veriler
);


-- ============================================================
-- 5. HAVA_DURUMU
--    Harici API'den saatlik çekilen meteorolojik veriler
-- ============================================================
CREATE TABLE hava_durumu (
    id            SERIAL         PRIMARY KEY,
    tarla_id      INTEGER        REFERENCES tarlalar(id),
    olcum_zamani  TIMESTAMPTZ    NOT NULL,
    sicaklik      DECIMAL(5,2),  -- °C
    nem           DECIMAL(5,2),  -- %
    yagis_mm      DECIMAL(6,2),  -- mm
    ruzgar_hizi   DECIMAL(5,2),  -- km/s
    veri_kaynagi  VARCHAR(50)    -- OpenWeatherMap | MGM
);


-- ============================================================
-- 6. TAVSIYELER
--    ML modelinin ürettiği sulama/gübreleme/ilaçlama önerileri
-- ============================================================
CREATE TABLE tavsiyeler (
    id                      SERIAL        PRIMARY KEY,
    tarla_id                INTEGER       REFERENCES tarlalar(id),
    olusturulma_zamani      TIMESTAMPTZ   DEFAULT NOW(),
    tavsiye_tipi            VARCHAR(50),  -- sulama | gübreleme | ilaçlama
    aciliyet                VARCHAR(20),  -- dusuk | orta | yuksek | kritik
    durum                   VARCHAR(20)   DEFAULT 'bekliyor',  -- bekliyor | uygulandı | reddedildi
    uygulayan_kullanici_id  INTEGER       REFERENCES kullanicilar(id)
);


-- ============================================================
-- İNDEKSLER – Performans optimizasyonu
-- ============================================================

-- olcumler: zaman aralığı sorguları için
CREATE INDEX idx_olcumler_zaman    ON olcumler(olcum_zamani DESC);

-- olcumler: sensör bazlı sorgular için
CREATE INDEX idx_olcumler_sensor   ON olcumler(sensor_id);

-- olcumler: tarla bazlı raporlar için
CREATE INDEX idx_olcumler_tarla    ON olcumler(tarla_id);

-- olcumler: bileşik indeks – "şu sensörün son 24 saati" gibi sorgular
CREATE INDEX idx_olcumler_bilesen  ON olcumler(sensor_id, olcum_zamani DESC);

-- hava_durumu: tarla + zaman kombinasyonu
CREATE INDEX idx_hava_tarla_zaman  ON hava_durumu(tarla_id, olcum_zamani DESC);

-- tavsiyeler: bekleyen tavsiyeleri dashboard'da filtrelemek için
CREATE INDEX idx_tavsiye_durum     ON tavsiyeler(durum);


-- ============================================================
-- SON
-- ============================================================
