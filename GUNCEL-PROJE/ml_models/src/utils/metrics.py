"""Degerlendirme metrikleri."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "rmse": round(rmse, 4),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
    }


def metrics_meet_threshold(metrics: dict[str, float], min_r2: float = 0.7) -> bool:
    return metrics.get("r2", 0) >= min_r2
