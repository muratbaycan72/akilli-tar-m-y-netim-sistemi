"""Toprak nemi tahmin servisi."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from src.utils.model_io import load_metadata, load_scaler, predict_with_coefficients


class SoilMoisturePredictor:
    """Egitilmis model ile toprak nemi tahmini."""

    def __init__(self, model_dir: Path) -> None:
        self.model_dir = Path(model_dir)
        self.metadata = load_metadata(self.model_dir)
        self.scaler = load_scaler(self.model_dir)
        self._keras_model: tf.keras.Model | None = None

    @property
    def feature_names(self) -> list[str]:
        return self.metadata["feature_names"]

    @property
    def model_version(self) -> str:
        return self.metadata["model_version"]

    def _load_keras(self) -> tf.keras.Model:
        if self._keras_model is None:
            self._keras_model = tf.keras.models.load_model(self.model_dir / "model.keras")
        return self._keras_model

    def predict(self, features: dict[str, float], use_keras: bool = False) -> dict[str, Any]:
        missing = [f for f in self.feature_names if f not in features]
        if missing:
            raise ValueError(f"Eksik ozellikler: {missing}")

        if use_keras:
            model = self._load_keras()
            x = np.array([[features[f] for f in self.feature_names]], dtype=np.float32)
            x_scaled = self.scaler.transform(x)
            value = float(model.predict(x_scaled, verbose=0).flatten()[0])
        else:
            value = predict_with_coefficients(features, self.metadata)

        value = round(max(0.0, min(100.0, value)), 2)
        confidence = self._estimate_confidence(value)

        return {
            "predicted_soil_moisture": value,
            "unit": "%",
            "confidence": confidence,
            "model_name": self.metadata["model_name"],
            "model_version": self.model_version,
            "input_features": features,
        }

    def _estimate_confidence(self, predicted_value: float) -> float:
        """R2 skoruna dayali guven tahmini."""
        r2 = self.metadata.get("metrics", {}).get("r2", 0.75)
        base = min(max(r2, 0.5), 0.99)
        # Asiri degerlerde guveni dusur
        if predicted_value < 15 or predicted_value > 80:
            base *= 0.9
        return round(base, 3)


def get_default_predictor() -> SoilMoisturePredictor:
    model_dir = Path(__file__).resolve().parents[2] / "saved_models" / "soil_moisture_v1"
    return SoilMoisturePredictor(model_dir)
