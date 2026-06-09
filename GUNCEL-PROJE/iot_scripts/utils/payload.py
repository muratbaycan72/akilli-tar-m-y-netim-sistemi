"""Sensör MQTT payload olusturma ve dogrulama yardimcilari."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {"device_id", "sensor_type", "value", "unit", "timestamp"}
VALID_SENSOR_TYPES = {
    "soil_moisture",
    "temperature",
    "humidity",
    "light",
    "ph",
    "plant_health",
}
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "sensor_payload.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_sensor_payload(
    *,
    device_id: str,
    field_id: str,
    sensor_type: str,
    value: float,
    unit: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if sensor_type not in VALID_SENSOR_TYPES:
        raise ValueError(f"Gecersiz sensor_type: {sensor_type}")

    payload: dict[str, Any] = {
        "device_id": device_id,
        "field_id": field_id,
        "sensor_type": sensor_type,
        "value": round(float(value), 4),
        "unit": unit,
        "timestamp": utc_now_iso(),
    }
    if metadata:
        payload["metadata"] = metadata
    return payload


def serialize_payload(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def parse_payload(raw: str | bytes) -> dict[str, Any]:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Payload JSON nesnesi olmali")
    return data


def validate_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []

    missing = REQUIRED_FIELDS - set(payload.keys())
    if missing:
        errors.append(f"Eksik alanlar: {', '.join(sorted(missing))}")

    sensor_type = payload.get("sensor_type")
    if sensor_type and sensor_type not in VALID_SENSOR_TYPES:
        errors.append(f"Gecersiz sensor_type: {sensor_type}")

    value = payload.get("value")
    if value is not None and not isinstance(value, (int, float)):
        errors.append("value sayisal olmali")

    timestamp = payload.get("timestamp")
    if timestamp:
        try:
            datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        except ValueError:
            errors.append("timestamp ISO-8601 formatinda olmali")

    return len(errors) == 0, errors
