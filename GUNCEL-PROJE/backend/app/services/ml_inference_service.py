"""ML model cikarim servisi (hafif - TensorFlow gerektirmez)."""
from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)

class MLInferenceService:
    """metadata.json katsayilari ile toprak nemi tahmini."""
    def __init__(self, model_dir: Path | None = None) -> None:
        if model_dir is not None:
            self.model_dir = model_dir
        else:
            backend_root = Path(__file__).resolve().parents[2]
            project_root = backend_root.parent
            self.model_dir = project_root / "ml_models" / "saved_models" / "soil_moisture_v1"
        self.metadata: dict[str, Any] | None = None
        self._load_metadata()

    def _load_metadata(self) -> None:
        metadata_path = self.model_dir / "metadata.json"
        if not metadata_path.exists():
            logger.warning("ML model metadata bulunamadi: %s", metadata_path)
            return
        with open(metadata_path, encoding="utf-8") as file:
            self.metadata = json.load(file)
        logger.info(
            "ML model yuklendi: %s v%s (R2=%s)",
            self.metadata.get("model_name"),
            self.metadata.get("model_version"),
            self.metadata.get("metrics", {}).get("r2"),
        )

    @property
    def is_ready(self) -> bool:
        return self.metadata is not None and "coefficients" in self.metadata

    def predict_soil_moisture(self, features: dict[str, float]) -> dict[str, Any]:
        if not self.is_ready:
            raise RuntimeError(
                f"ML model yuklenemedi. Once ml_models egitimini calistirin: {self.model_dir}"
            )
        meta = self.metadata
        coef = meta["coefficients"]
        names = coef["feature_names"]
        missing = [f for f in names if f not in features]
        if missing:
            raise ValueError(f"Eksik ozellikler: {missing}")
        mean = np.array(coef["scaler_mean"])
        scale = np.array(coef["scaler_scale"])
        weights = np.array(coef["weights"])
        bias = coef["bias"]
        x = np.array([features[name] for name in names], dtype=np.float64)
        x_scaled = (x - mean) / scale
        value = float(np.dot(x_scaled, weights) + bias)
        value = round(max(0.0, min(100.0, value)), 2)
        r2 = meta.get("metrics", {}).get("r2", 0.75)
        confidence = round(min(max(r2, 0.5), 0.99), 3)
        return {
            "predicted_value": value,
            "confidence": confidence,
            "model_name": meta["model_name"],
            "model_version": meta["model_version"],
            "input_features": features,
        }

# FIX: Lazy singleton — import sirasinda degil, ilk kullanımda olusturulur
_ml_service: MLInferenceService | None = None

def get_ml_service() -> MLInferenceService:
    global _ml_service
    if _ml_service is None:
        _ml_service = MLInferenceService()
    return _ml_service

# Geriye donuk uyumluluk icin ml_service alias'i
class _LazyService:
    def __getattr__(self, name):
        return getattr(get_ml_service(), name)

ml_service = _LazyService()