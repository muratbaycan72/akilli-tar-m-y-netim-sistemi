"""Model kaydetme ve yukleme."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler


def save_artifacts(
    model_dir: Path,
    keras_model: Any,
    scaler: StandardScaler,
    metadata: dict[str, Any],
) -> None:
    model_dir.mkdir(parents=True, exist_ok=True)
    keras_model.save(model_dir / "model.keras")
    joblib.dump(scaler, model_dir / "scaler.pkl")

    weights, bias = keras_model.layers[0].get_weights()
    metadata["coefficients"] = {
        "weights": weights.flatten().tolist(),
        "bias": float(bias.flatten()[0]),
        "feature_names": metadata.get("feature_names", []),
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
    }

    with open(model_dir / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)


def load_metadata(model_dir: Path) -> dict[str, Any]:
    with open(model_dir / "metadata.json", encoding="utf-8") as file:
        return json.load(file)


def load_scaler(model_dir: Path) -> StandardScaler:
    return joblib.load(model_dir / "scaler.pkl")


def predict_with_coefficients(features: dict[str, float], metadata: dict[str, Any]) -> float:
    """TensorFlow olmadan hafif tahmin (backend icin)."""
    coef = metadata["coefficients"]
    names = coef["feature_names"]
    mean = np.array(coef["scaler_mean"])
    scale = np.array(coef["scaler_scale"])
    weights = np.array(coef["weights"])
    bias = coef["bias"]

    x = np.array([features[name] for name in names], dtype=np.float64)
    x_scaled = (x - mean) / scale
    return float(np.dot(x_scaled, weights) + bias)
