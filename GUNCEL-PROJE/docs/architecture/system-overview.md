# Sistem Mimarisi

## Genel Bakis

Akilli Tarim Yonetim Sistemi, moduler monolith mimarisi uzerine kurulmustur.
Her modul bagimsiz gelistirilebilir ve ileride microservice'lere ayrilabilir.

## Veri Akisi

```
Sensörler/Simulator → MQTT Broker → Backend (MQTT Bridge) → PostgreSQL
                                              ↓
                                        ML Inference
                                              ↓
                                    Web / Mobil API
```

## Servisler

| Servis | Port | Aciklama |
|--------|------|----------|
| PostgreSQL | 5432 | Ana veritabani |
| Mosquitto MQTT | 1883 | IoT mesaj broker |
| Backend API | 8000 | REST + WebSocket |
| React Web | 5173 | Vite dev server |
| React Native | 8081 | Expo dev server |

## Veritabani Tablolari

- `users` - Kullanici hesaplari
- `fields` - Tarla/alan tanimlari
- `sensors` - Sensör cihazlari
- `sensor_readings` - Zaman serisi sensör verileri
- `weather_readings` - Hava durumu kayitlari
- `plant_health_records` - Bitki sagligi
- `irrigation_logs` / `fertilization_logs` / `spraying_logs` - Operasyon kayitlari
- `ml_predictions` - ML tahmin sonuclari
- `alerts` - Bildirimler
