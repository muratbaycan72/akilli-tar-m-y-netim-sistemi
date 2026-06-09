# ML Models

TensorFlow tabanli makine ogrenimi modelleri ve egitim pipeline.

## Toprak Nemi Regresyon Modeli

| Ozellik | Deger |
|---------|-------|
| Algoritma | Linear Regression (TensorFlow/Keras) |
| Giris | temperature, humidity, rainfall_mm, wind_speed, solar_radiation |
| Cikis | soil_moisture (%) |
| Metrikler | MAE, RMSE, R2 |

## Kurulum

```bash
cd ml_models
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Model Egitimi

```bash
python -m src.training.train_regressor
```

Opsiyonlar:

```bash
python -m src.training.train_regressor --epochs 150
python -m src.training.train_regressor --use-db    # PostgreSQL'den veri
python -m src.training.train_regressor --quiet
```

Egitim sonrasi `saved_models/soil_moisture_v1/` altina kaydedilir:
- `model.keras` - TensorFlow modeli
- `scaler.pkl` - StandardScaler
- `metadata.json` - Metrikler ve katsayilar (backend inference icin)

## Model Degerlendirme

```bash
python -m src.training.evaluate
```

## Tahmin (CLI)

```python
from src.inference.predictor import get_default_predictor

predictor = get_default_predictor()
result = predictor.predict({
    "temperature": 28.0,
    "humidity": 55.0,
    "rainfall_mm": 3.0,
    "wind_speed": 12.0,
    "solar_radiation": 600.0,
})
print(result)
```

## Backend Entegrasyonu

Backend API uzerinden tahmin:

```bash
POST /api/v1/predictions/soil-moisture
{
  "field_id": "...",
  "temperature": 28.0,
  "humidity": 55.0,
  "rainfall_mm": 3.0,
  "wind_speed": 12.0,
  "solar_radiation": 600.0
}
```

## Test

```bash
pytest tests/ -v
```
