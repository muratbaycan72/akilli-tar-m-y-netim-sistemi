"""ML pipeline testleri."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import TrainingConfig
from src.data.preprocessor import prepare_data
from src.data.synthetic_generator import generate_synthetic_dataset
from src.utils.metrics import compute_metrics, metrics_meet_threshold
from src.utils.model_io import load_metadata, predict_with_coefficients

try:
    import tensorflow as tf
    HAS_TF = True
except ImportError:
    HAS_TF = False


@pytest.fixture
def sample_df():
    return generate_synthetic_dataset(n_samples=500, random_seed=42)


@pytest.fixture
def training_config(tmp_path):
    return TrainingConfig(
        model_name="test_model",
        model_version="0.0.1",
        features=["temperature", "humidity", "rainfall_mm", "wind_speed", "solar_radiation"],
        target="soil_moisture",
        epochs=5,
        batch_size=32,
        learning_rate=0.05,
        validation_split=0.2,
        random_seed=42,
        synthetic_samples=500,
        test_size=0.2,
        use_database=False,
        saved_model_dir=tmp_path / "model",
    )


class TestSyntheticData:
    def test_generate_dataset_shape(self, sample_df):
        assert len(sample_df) == 500
        assert "soil_moisture" in sample_df.columns

    def test_moisture_in_valid_range(self, sample_df):
        assert sample_df["soil_moisture"].min() >= 10
        assert sample_df["soil_moisture"].max() <= 85


class TestPreprocessor:
    def test_prepare_data_shapes(self, sample_df, training_config):
        prepared = prepare_data(
            sample_df,
            training_config.features,
            training_config.target,
            test_size=0.2,
        )
        assert prepared.x_train.shape[1] == len(training_config.features)
        assert len(prepared.y_train) + len(prepared.y_test) == len(sample_df)


class TestModelTraining:
    @pytest.mark.skipif(not HAS_TF, reason="TensorFlow yuklu degil")
    def test_train_and_predict(self, sample_df, training_config):
        from src.models.soil_moisture_regressor import build_soil_moisture_model, train_model

        prepared = prepare_data(
            sample_df,
            training_config.features,
            training_config.target,
            test_size=0.2,
            random_seed=42,
        )
        model = build_soil_moisture_model(len(training_config.features), learning_rate=0.05)
        train_model(
            model,
            prepared.x_train,
            prepared.y_train,
            epochs=10,
            batch_size=32,
            validation_split=0.2,
            verbose=0,
        )
        y_pred = model.predict(prepared.x_test, verbose=0).flatten()
        metrics = compute_metrics(prepared.y_test, y_pred)
        assert metrics["r2"] > 0.5
        assert metrics["mae"] < 10

    @pytest.mark.skipif(not HAS_TF, reason="TensorFlow yuklu degil")
    def test_save_and_lightweight_predict(self, sample_df, training_config):
        from src.models.soil_moisture_regressor import build_soil_moisture_model, train_model
        from src.utils.model_io import save_artifacts

        prepared = prepare_data(
            sample_df,
            training_config.features,
            training_config.target,
            test_size=0.2,
        )
        model = build_soil_moisture_model(len(training_config.features))
        train_model(
            model, prepared.x_train, prepared.y_train,
            epochs=5, batch_size=32, validation_split=0.2, verbose=0,
        )
        metadata = {
            "model_name": "test",
            "model_version": "0.0.1",
            "feature_names": training_config.features,
            "metrics": {"r2": 0.8},
        }
        save_artifacts(training_config.saved_model_dir, model, prepared.scaler, metadata)

        features = {
            "temperature": 25.0,
            "humidity": 60.0,
            "rainfall_mm": 5.0,
            "wind_speed": 10.0,
            "solar_radiation": 500.0,
        }
        loaded = load_metadata(training_config.saved_model_dir)
        prediction = predict_with_coefficients(features, loaded)
        assert 0 <= prediction <= 100

    def test_metadata_inference(self):
        model_dir = ROOT / "saved_models" / "soil_moisture_v1"
        if not (model_dir / "metadata.json").exists():
            pytest.skip("metadata.json yok")
        loaded = load_metadata(model_dir)
        prediction = predict_with_coefficients(
            {
                "temperature": 25.0,
                "humidity": 60.0,
                "rainfall_mm": 5.0,
                "wind_speed": 10.0,
                "solar_radiation": 500.0,
            },
            loaded,
        )
        assert 0 <= prediction <= 100


class TestMetrics:
    def test_perfect_prediction(self):
        y = np.array([1.0, 2.0, 3.0])
        metrics = compute_metrics(y, y)
        assert metrics["mae"] == 0.0
        assert metrics["r2"] == 1.0

    def test_quality_threshold(self):
        assert metrics_meet_threshold({"r2": 0.85}) is True
        assert metrics_meet_threshold({"r2": 0.5}) is False
