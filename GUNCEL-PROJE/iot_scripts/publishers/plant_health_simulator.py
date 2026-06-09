"""Bitki sagligi sensör simulatörü."""

from __future__ import annotations

import argparse
import logging
import random

from publishers.base_publisher import BasePublisher

logger = logging.getLogger(__name__)


class PlantHealthSimulator(BasePublisher):
    sensor_type = "plant_health"
    unit = "score"
    topic_key = "plant_health"

    def __init__(self, device_id: str = "plant-001", field_id: str | None = None) -> None:
        super().__init__(device_id=device_id, field_id=field_id)
        self._current = random.uniform(70.0, 90.0)

    def generate_value(self) -> float:
        self._current += random.uniform(-3.0, 2.0)
        self._current = max(30.0, min(100.0, self._current))
        return round(self._current, 2)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Bitki sagligi MQTT simulatörü")
    parser.add_argument("--field-id", default=None)
    parser.add_argument("--device-id", default="plant-001")
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--count", type=int, default=None)
    args = parser.parse_args()

    simulator = PlantHealthSimulator(device_id=args.device_id, field_id=args.field_id)
    simulator.run(interval_seconds=args.interval, max_messages=args.count)


if __name__ == "__main__":
    main()
