# Frontend (React Web Dashboard)

Modern web tabanlı tarım yönetim dashboard'u.

## Kurulum

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Uygulama: http://localhost:5173

## Sayfalar

| Sayfa | Açıklama |
|-------|----------|
| Dashboard | Özet istatistikler, grafikler, tarla bilgisi |
| Sensörler | Zaman serisi çizgi grafikleri, son okumalar tablosu |
| ML Tahminler | Toprak nemi tahmini formu, model metrikleri |
| Kontrol Paneli | Manuel sulama tetikleme, sulama geçmişi |
| Alarmlar | Bildirim listesi |

## Teknolojiler

- React 19 + TypeScript
- Vite 6
- Recharts (çizgi/çubuk grafikler)
- React Router 7

## Backend Bağlantısı

`.env` dosyasında API adresi:

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Vite dev server `/api` isteklerini backend'e proxy eder.

## Geliştirme

Backend ve seed verisi çalışıyor olmalı:

```bash
# Terminal 1 - Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```
