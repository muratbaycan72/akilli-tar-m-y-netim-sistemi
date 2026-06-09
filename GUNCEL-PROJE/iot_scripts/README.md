# IoT Scripts

MQTT tabanli sensör veri toplama ve simulasyon modulu.

## Kurulum

```bash
cd iot_scripts
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Broker'in calistigindan emin olun:

```bash
cd ..
docker compose up -d mosquitto
```

## MQTT Topic Yapisi

```
akilli-tarim/{field_id}/sensors/soil_moisture
akilli-tarim/{field_id}/sensors/temperature
akilli-tarim/{field_id}/sensors/humidity
akilli-tarim/{field_id}/sensors/plant_health
akilli-tarim/{field_id}/commands/irrigation
```

## Kullanim

### Subscriber (veri dinle)

```bash
cd iot_scripts
python run_subscriber.py
```

### Tekil simulatörler

```bash
python -m publishers.soil_moisture_simulator --interval 3 --count 10
python -m publishers.weather_simulator --interval 3 --count 10
python -m publishers.plant_health_simulator --interval 5 --count 5
```

### Tum simulatörleri birlikte calistir

```bash
python run_publishers.py --interval 5
```

## Test

```bash
pytest tests/ -v
```

## Modul Yapisi

| Dosya | Gorev |
|-------|-------|
| `publishers/base_publisher.py` | Ortak MQTT yayinci sinifi |
| `publishers/soil_moisture_simulator.py` | Toprak nemi simulatörü |
| `publishers/weather_simulator.py` | Sicaklik + nem simulatörü |
| `publishers/plant_health_simulator.py` | Bitki sagligi simulatörü |
| `subscribers/mqtt_client.py` | MQTT dinleyici istemci |
| `subscribers/data_ingestion_handler.py` | Payload dogrulama ve istatistik |
| `utils/config_loader.py` | YAML + .env yapilandirma |
| `utils/payload.py` | JSON payload olusturma/dogrulama |
