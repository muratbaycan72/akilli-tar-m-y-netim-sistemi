"""Backend testleri."""

from __future__ import annotations

import os
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import (
    FieldCreate,
    IrrigationCreate,
    SensorCreate,
    SensorReadingCreate,
    SensorType,
    UserCreate,
)


class TestSchemas:
    def test_user_create_valid(self):
        user = UserCreate(email="test@tarim.com", full_name="Test User", password="secret1")
        assert user.email == "test@tarim.com"

    def test_user_create_short_password(self):
        with pytest.raises(ValidationError):
            UserCreate(email="test@tarim.com", full_name="Test", password="123")

    def test_sensor_create_valid(self):
        sensor = SensorCreate(
            field_id="00000000-0000-0000-0000-000000000001",
            sensor_type=SensorType.soil_moisture,
            device_id="soil-001",
            unit="%",
        )
        assert sensor.sensor_type == SensorType.soil_moisture

    def test_irrigation_duration_must_be_positive(self):
        with pytest.raises(ValidationError):
            IrrigationCreate(field_id="abc", duration_minutes=0)

    def test_field_create(self):
        field = FieldCreate(user_id="u1", name="Tarla 1", crop_type="misir")
        assert field.name == "Tarla 1"


@pytest.fixture
def api_client():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from app.main import app

    return TestClient(app)


class TestAPI:
    def test_health_check(self, api_client):
        response = api_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @pytest.mark.skipif(
        os.getenv("SKIP_DB_TESTS", "1") == "1",
        reason="PostgreSQL gerektirir (SKIP_DB_TESTS=0 ile calistirin)",
    )
    def test_create_and_list_fields(self, api_client):
        user_resp = api_client.post(
            "/api/v1/users",
            json={"email": "apitest@tarim.com", "full_name": "API Test", "password": "test1234"},
        )
        assert user_resp.status_code == 201
        user_id = user_resp.json()["id"]

        field_resp = api_client.post(
            "/api/v1/fields",
            json={"user_id": user_id, "name": "Test Tarla", "crop_type": "bugday"},
        )
        assert field_resp.status_code == 201
        field_id = field_resp.json()["id"]

        list_resp = api_client.get(f"/api/v1/fields?user_id={user_id}")
        assert list_resp.status_code == 200
        assert any(f["id"] == field_id for f in list_resp.json())

    @pytest.mark.skipif(
        os.getenv("SKIP_DB_TESTS", "1") == "1",
        reason="PostgreSQL gerektirir",
    )
    def test_sensor_reading_crud(self, api_client):
        user = api_client.post(
            "/api/v1/users",
            json={"email": "sensor@tarim.com", "full_name": "Sensor Test", "password": "test1234"},
        ).json()
        field = api_client.post(
            "/api/v1/fields",
            json={"user_id": user["id"], "name": "Sensor Tarla"},
        ).json()
        sensor = api_client.post(
            "/api/v1/sensors",
            json={
                "field_id": field["id"],
                "sensor_type": "soil_moisture",
                "device_id": "test-soil-001",
                "unit": "%",
            },
        ).json()

        reading_resp = api_client.post(
            "/api/v1/sensors/readings",
            json={
                "sensor_id": sensor["id"],
                "field_id": field["id"],
                "value": 45.2,
                "unit": "%",
                "recorded_at": datetime.utcnow().isoformat(),
            },
        )
        assert reading_resp.status_code == 201
        assert reading_resp.json()["value"] == 45.2
