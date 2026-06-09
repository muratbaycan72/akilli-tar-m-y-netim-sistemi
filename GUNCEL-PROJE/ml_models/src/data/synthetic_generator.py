"""Sentetik egitim verisi uretici."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_synthetic_dataset(n_samples: int = 2000, random_seed: int = 42) -> pd.DataFrame:
    """
    Toprak nemi ile iliskili sentetik sensör verisi uretir.

    Gercek tarim iliskilerini taklit eder:
    - Yuksek sicaklik -> dusuk nem (buharlasma)
    - Yuksek hava nemi / yagis -> yuksek toprak nemi
    """
    rng = np.random.default_rng(random_seed)

    temperature = rng.uniform(10, 38, n_samples)
    humidity = rng.uniform(25, 95, n_samples)
    rainfall_mm = rng.exponential(scale=3.0, size=n_samples)
    rainfall_mm = np.clip(rainfall_mm, 0, 30)
    wind_speed = rng.uniform(0, 25, n_samples)
    solar_radiation = rng.uniform(100, 900, n_samples)

    soil_moisture = (
        35.0
        + 0.35 * humidity
        - 0.55 * temperature
        + 1.2 * rainfall_mm
        - 0.15 * wind_speed
        - 0.008 * solar_radiation
        + rng.normal(0, 2.5, n_samples)
    )
    soil_moisture = np.clip(soil_moisture, 10, 85)

    return pd.DataFrame(
        {
            "temperature": np.round(temperature, 2),
            "humidity": np.round(humidity, 2),
            "rainfall_mm": np.round(rainfall_mm, 2),
            "wind_speed": np.round(wind_speed, 2),
            "solar_radiation": np.round(solar_radiation, 2),
            "soil_moisture": np.round(soil_moisture, 2),
        }
    )
