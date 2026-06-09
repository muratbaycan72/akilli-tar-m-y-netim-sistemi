"""Gelen MQTT mesajlarini dogrulayan ve isleyen handler."""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from utils.payload import parse_payload, validate_payload

logger = logging.getLogger(__name__)


@dataclass
class IngestionStats:
    total_received: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    by_sensor_type: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_readings: dict[str, dict[str, Any]] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "total_received": self.total_received,
            "valid_count": self.valid_count,
            "invalid_count": self.invalid_count,
            "by_sensor_type": dict(self.by_sensor_type),
            "last_readings": self.last_readings,
        }


class DataIngestionHandler:
    """MQTT mesajlarini parse eder, dogrular ve istatistik tutar."""

    def __init__(self) -> None:
        self.stats = IngestionStats()

    def handle(self, topic: str, raw_payload: str | bytes) -> dict[str, Any] | None:
        self.stats.total_received += 1

        try:
            payload = parse_payload(raw_payload)
        except (ValueError, UnicodeDecodeError) as exc:
            self.stats.invalid_count += 1
            logger.warning("Parse hatasi | topic=%s | error=%s", topic, exc)
            return None

        is_valid, errors = validate_payload(payload)
        if not is_valid:
            self.stats.invalid_count += 1
            logger.warning("Dogrulama hatasi | topic=%s | errors=%s", topic, errors)
            return None

        sensor_type = payload["sensor_type"]
        self.stats.valid_count += 1
        self.stats.by_sensor_type[sensor_type] += 1
        self.stats.last_readings[sensor_type] = {
            "topic": topic,
            "value": payload["value"],
            "unit": payload["unit"],
            "field_id": payload.get("field_id"),
            "device_id": payload["device_id"],
            "timestamp": payload["timestamp"],
            "received_at": datetime.now(timezone.utc).isoformat(),
        }

        logger.info(
            "Gecerli veri | %s | %s=%s %s | field=%s",
            sensor_type,
            payload["device_id"],
            payload["value"],
            payload["unit"],
            payload.get("field_id"),
        )
        return payload

    def create_callback(self):
        """MqttSubscriber icin callback factory."""

        def callback(topic: str, raw_payload: bytes) -> None:
            self.handle(topic, raw_payload)

        return callback
