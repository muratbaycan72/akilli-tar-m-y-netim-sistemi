# Backend API

Python tabanli REST API ve PostgreSQL CRUD katmani (psycopg2 + FastAPI).

## Kurulum

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp ..\.env.example ..\.env
```

PostgreSQL ve MQTT broker calisiyor olmali:

```bash
cd ..
docker compose up -d
```

## Veritabani Seed

```bash
python scripts/seed_data.py
```

## API Baslat

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: http://localhost:8000/docs

## API Endpoint'leri

| Method | Endpoint | Aciklama |
|--------|----------|----------|
| GET | `/health` | Saglik kontrolu |
| POST/GET | `/api/v1/users` | Kullanici CRUD |
| POST/GET/PUT/DELETE | `/api/v1/fields` | Tarla yonetimi |
| POST/GET | `/api/v1/sensors` | Sensör yonetimi |
| POST/GET | `/api/v1/sensors/readings` | Sensör okumalari |
| GET | `/api/v1/sensors/readings/latest` | Son okumalar |
| POST/GET | `/api/v1/irrigation` | Sulama kayitlari |
| POST/GET | `/api/v1/fertilization` | Gubreleme kayitlari |
| POST/GET | `/api/v1/spraying` | Ilaclama kayitlari |
| POST/GET | `/api/v1/predictions` | ML tahminleri |
| POST/GET | `/api/v1/alerts` | Alarmlar |

## Moduller

- `app/db/crud/` - psycopg2 ile CRUD fonksiyonlari
- `app/api/v1/` - REST endpoint'leri
- `app/services/mqtt_bridge.py` - MQTT -> PostgreSQL koprusu
- `app/schemas/` - Pydantic DTO'lar

## Test

```bash
pytest tests/ -v
# PostgreSQL ile entegrasyon testleri:
$env:SKIP_DB_TESTS=0; pytest tests/test_api.py -v
```
