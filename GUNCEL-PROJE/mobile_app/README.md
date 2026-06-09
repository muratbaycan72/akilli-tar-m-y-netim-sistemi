# Mobile App (React Native + Expo)

iOS ve Android için akıllı tarım yönetim mobil uygulaması.

## Kurulum

```bash
cd mobile_app
npm install
cp .env.example .env
npx expo start
```

Expo Go uygulaması ile QR kodu tarayın veya emülatörde çalıştırın:

```bash
npx expo start --android
npx expo start --ios
```

## API Bağlantısı

`.env` dosyasında backend adresini ayarlayın:

| Ortam | EXPO_PUBLIC_API_URL |
|-------|---------------------|
| Android Emülatör | `http://10.0.2.2:8000/api/v1` |
| iOS Simülatör | `http://localhost:8000/api/v1` |
| Fiziksel Cihaz | `http://<BILGISAYAR-IP>:8000/api/v1` |

## Ekranlar

| Sekme | Açıklama |
|-------|----------|
| Ana Sayfa | Özet kartlar, anlık sensörler, düşük nem alarmı |
| Sensörler | Sensör listesi + detay grafikleri |
| Sulama | Manuel sulama tetikleme, geçmiş kayıtlar |
| Alarmlar | Bildirim listesi |
| Ayarlar | Tarla seçimi, API yapılandırması |

## Özellikler

- React Navigation (Tab + Stack)
- 30 sn otomatik veri yenileme
- Uygulama ön plana gelince senkronizasyon
- Expo Notifications (yerel bildirimler)
- react-native-chart-kit mini grafikler

## Gereksinimler

Backend API çalışıyor olmalı:

```bash
cd backend && uvicorn app.main:app --reload --host 0.0.0.0
```

`--host 0.0.0.0` fiziksel cihazdan erişim için gereklidir.
