"""MQTT payload ve ingestion handler testleri."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from subscribers.data_ingestion_handler import DataIngestionHandler
from utils.config_loader import load_mqtt_config, load_topic_config
from utils.payload import build_sensor_payload, parse_payload, validate_payload


class TestPayload:
    def test_build_valid_payload(self):
        payload = build_sensor_payload(
            device_id="soil-001",
            field_id="field-001",
            sensor_type="soil_moisture",
            value=42.5,
            unit="%",
        )
        is_valid, errors = validate_payload(payload)
        assert is_valid is True
        assert errors == []
        assert payload["sensor_type"] == "soil_moisture"

    def test_invalid_sensor_type_raises(self):
        with pytest.raises(ValueError, match="Gecersiz sensor_type"):
            build_sensor_payload(
                device_id="x",
                field_id="field-001",
                sensor_type="invalid",
                value=1.0,
                unit="%",
            )

    def test_missing_required_field(self):
        payload = {"device_id": "x", "sensor_type": "humidity", "value": 50, "unit": "%"}
        is_valid, errors = validate_payload(payload)
        assert is_valid is False
        assert any("timestamp" in err for err in errors)

    def test_roundtrip_serialize_parse(self):
        payload = build_sensor_payload(
            device_id="weather-001",
            field_id="field-001",
            sensor_type="temperature",
            value=24.3,
            unit="C",
        )
        raw = json.dumps(payload)
        parsed = parse_payload(raw)
        is_valid, _ = validate_payload(parsed)
        assert is_valid is True
        assert parsed["value"] == 24.3


class TestConfigLoader:
    def test_load_mqtt_config(self):
        config = load_mqtt_config()
        assert config.broker_host
        assert config.broker_port == 1883
        assert config.qos >= 0

    def test_build_topic(self):
        topics = load_topic_config()
        topic = topics.build_topic("soil_moisture", "field-001")
        assert topic == "akilli-tarim/field-001/sensors/soil_moisture"
        assert topics.sensor_wildcard() == "akilli-tarim/+/sensors/#"


class TestDataIngestionHandler:
    def test_handle_valid_message(self):
        handler = DataIngestionHandler()
        payload = build_sensor_payload(
            device_id="soil-001",
            field_id="field-001",
            sensor_type="soil_moisture",
            value=40.0,
            unit="%",
        )
        result = handler.handle("akilli-tarim/field-001/sensors/soil_moisture", json.dumps(payload))
        assert result is not None
        assert handler.stats.valid_count == 1
        assert handler.stats.by_sensor_type["soil_moisture"] == 1

    def test_handle_invalid_json(self):
        handler = DataIngestionHandler()
        result = handler.handle("topic", "not-json")
        assert result is None
        assert handler.stats.invalid_count == 1

    def test_handle_invalid_payload(self):
        handler = DataIngestionHandler()
        result = handler.handle("topic", json.dumps({"device_id": "x"}))
        assert result is None
        assert handler.stats.invalid_count == 1
