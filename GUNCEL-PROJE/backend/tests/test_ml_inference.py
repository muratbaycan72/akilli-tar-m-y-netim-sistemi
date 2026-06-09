"""ML inference servisi testleri."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.services.ml_inference_service import MLInferenceService


@pytest.fixture
def ml_service():
    project_root = Path(__file__).resolve().parents[2]
    model_dir = project_root / "ml_models" / "saved_models" / "soil_moisture_v1"
    if not (model_dir / "metadata.json").exists():
        pytest.skip("ML model metadata yok")
    return MLInferenceService(model_dir=model_dir)


class TestMLInference:
    def test_model_is_ready(self, ml_service):
        assert ml_service.is_ready is True

    def test_predict_soil_moisture(self, ml_service):
        result = ml_service.predict_soil_moisture(
            {
                "temperature": 25.0,
                "humidity": 60.0,
                "rainfall_mm": 5.0,
                "wind_speed": 10.0,
                "solar_radiation": 500.0,
            }
        )
        assert 0 <= result["predicted_value"] <= 100
        assert 0 < result["confidence"] <= 1
        assert result["model_name"] == "soil_moisture_regressor"

    def test_missing_features_raises(self, ml_service):
        with pytest.raises(ValueError, match="Eksik ozellikler"):
            ml_service.predict_soil_moisture({"temperature": 25.0})
