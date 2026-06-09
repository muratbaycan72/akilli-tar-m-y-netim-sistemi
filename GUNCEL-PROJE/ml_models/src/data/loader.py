"""PostgreSQL'den egitim verisi yukleme."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv

from src.data.synthetic_generator import generate_synthetic_dataset

load_dotenv(Path(__file__).resolve().parents[3] / ".env")


def load_from_database(database_url: str | None = None) -> pd.DataFrame:
    """sensor_readings ve weather_readings tablolarindan veri ceker."""
    url = database_url or os.getenv(
        "DATABASE_URL",
        "postgresql://akilli_tarim:changeme_secure_password@localhost:5432/akilli_tarim_db",
    )
    query = """
        SELECT
            w.temperature,
            w.humidity,
            COALESCE(w.rainfall_mm, 0) AS rainfall_mm,
            COALESCE(w.wind_speed, 0) AS wind_speed,
            COALESCE(w.solar_radiation, 0) AS solar_radiation,
            sr.value AS soil_moisture
        FROM sensor_readings sr
        JOIN sensors s ON s.id = sr.sensor_id AND s.sensor_type = 'soil_moisture'
        JOIN weather_readings w ON w.field_id = sr.field_id
            AND w.recorded_at BETWEEN sr.recorded_at - INTERVAL '1 hour'
                                  AND sr.recorded_at + INTERVAL '1 hour'
        ORDER BY sr.recorded_at DESC
        LIMIT 10000
    """
    with psycopg2.connect(url) as conn:
        df = pd.read_sql(query, conn)

    if df.empty:
        raise ValueError("Veritabaninda yeterli eslesmis veri yok")

    return df


def load_training_data(use_database: bool = False, synthetic_samples: int = 2000) -> pd.DataFrame:
    if use_database:
        try:
            return load_from_database()
        except Exception:
            pass
    return generate_synthetic_dataset(n_samples=synthetic_samples)
