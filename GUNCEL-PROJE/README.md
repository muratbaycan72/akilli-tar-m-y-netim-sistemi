# Akıllı Tarım Yönetim Sistemi

Sensör verileri ve makine öğrenimi kullanarak tarım süreçlerini optimize eden modüler platform.

## Modüller

| Modül | Teknoloji | Açıklama |
|-------|-----------|----------|
| `iot_scripts/` | Python, MQTT | Sensör veri toplama ve simülasyon |
| `backend/` | Python, PostgreSQL | REST API, CRUD, iş mantığı |
| `ml_models/` | Python, TensorFlow | Tahmin modelleri ve eğitim pipeline |
| `frontend/` | React | Web dashboard ve kontrol paneli |
| `mobile_app/` | React Native | Mobil izleme ve uzaktan kontrol |

## Hızlı Başlangıç

### Gereksinimler

- Docker & Docker Compose
- Python 3.11+
- Node.js 20+ (frontend/mobil için, ileriki adımlarda)

### 1. Ortam Değişkenlerini Ayarla

```bash
cp .env.example .env
```

`.env` dosyasındaki şifreleri güvenli değerlerle güncelleyin.

### 2. Altyapıyı Başlat (PostgreSQL + MQTT)

```bash
docker compose up -d
```

Servis durumunu kontrol edin:

```bash
docker compose ps
```

### 3. Veritabanı Bağlantısını Doğrula

PostgreSQL ilk başlatmada `backend/scripts/init_db.sql` dosyasını otomatik çalıştırır.

```bash
docker compose exec postgres psql -U akilli_tarim -d akilli_tarim_db -c "\dt"
```

### 4. MQTT Broker'ı Doğrula

```bash
docker compose logs mosquitto
```

## Proje Yapısı

```
akilli-tarim-yonetim-sistemi/
├── backend/          # API ve veritabanı katmanı
├── frontend/         # React web arayüzü
├── mobile_app/       # React Native mobil uygulama
├── ml_models/        # TensorFlow ML modelleri
├── iot_scripts/      # MQTT sensör scriptleri
├── shared/           # Ortak tip ve sabitler
└── docs/             # Mimari dokümantasyon
```

## Geliştirme Yol Haritası

- [x] Adım 1: Proje iskeleti ve Docker altyapısı
- [x] Adım 2: IoT MQTT publisher/subscriber
- [x] Adım 3: Backend CRUD ve REST API
- [x] Adım 4: ML toprak nemi regresyon modeli
- [x] Adım 5: React web dashboard
- [x] Adım 6: React Native mobil uygulama

## Lisans

Bu proje eğitim ve geliştirme amaçlıdır.
