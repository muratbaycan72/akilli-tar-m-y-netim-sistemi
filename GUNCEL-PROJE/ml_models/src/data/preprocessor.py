"""Veri on isleme ve ozellik muhendisligi."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dataclass
class PreparedData:
    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    scaler: StandardScaler
    feature_names: list[str]


def prepare_data(
    df: pd.DataFrame,
    feature_names: list[str],
    target: str,
    test_size: float = 0.2,
    random_seed: int = 42,
) -> PreparedData:
    missing = [col for col in feature_names + [target] if col not in df.columns]
    if missing:
        raise ValueError(f"Eksik sutunlar: {missing}")

    x = df[feature_names].values.astype(np.float32)
    y = df[target].values.astype(np.float32)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_seed
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train).astype(np.float32)
    x_test_scaled = scaler.transform(x_test).astype(np.float32)

    return PreparedData(
        x_train=x_train_scaled,
        x_test=x_test_scaled,
        y_train=y_train,
        y_test=y_test,
        scaler=scaler,
        feature_names=feature_names,
    )
