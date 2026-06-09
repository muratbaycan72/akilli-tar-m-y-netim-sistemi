"""TensorFlow olmadan varsayilan model artifact'lerini olusturur (sklearn)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import TrainingConfig
from src.data.loader import load_training_data
from src.data.preprocessor import prepare_data
from src.utils.metrics import compute_metrics

OUTPUT_DIR = ROOT / "saved_models" / "soil_moisture_v1"


def bootstrap() -> dict:
    config = TrainingConfig.load()
    df = load_training_data(use_database=False, synthetic_samples=config.synthetic_samples)
    prepared = prepare_data(
        df, config.features, config.target,
        test_size=config.test_size, random_seed=config.random_seed,
    )

    reg = LinearRegression()
    reg.fit(prepared.x_train, prepared.y_train)
    y_pred = reg.predict(prepared.x_test)
    metrics = compute_metrics(prepared.y_test, y_pred)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(prepared.scaler, OUTPUT_DIR / "scaler.pkl")

    metadata = {
        "model_name": config.model_name,
        "model_version": config.model_version,
        "feature_names": config.features,
        "target": config.target,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "training_samples": len(prepared.x_train),
        "test_samples": len(prepared.x_test),
        "metrics": metrics,
        "epochs": config.epochs,
        "passed_quality_check": metrics.get("r2", 0) >= 0.7,
        "bootstrap": True,
        "note": "Sklearn bootstrap; TensorFlow egitimi icin train_regressor.py calistirin",
        "coefficients": {
            "weights": reg.coef_.tolist(),
            "bias": float(reg.intercept_),
            "feature_names": config.features,
            "scaler_mean": prepared.scaler.mean_.tolist(),
            "scaler_scale": prepared.scaler.scale_.tolist(),
        },
    }

    with open(OUTPUT_DIR / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)

    print(f"Bootstrap tamamlandi -> {OUTPUT_DIR}")
    print(f"Metrikler: MAE={metrics['mae']} RMSE={metrics['rmse']} R2={metrics['r2']}")
    return metadata


if __name__ == "__main__":
    bootstrap()
