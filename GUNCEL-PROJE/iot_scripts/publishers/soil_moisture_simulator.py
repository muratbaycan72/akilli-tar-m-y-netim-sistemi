"""Toprak nemi sensör simulatörü."""

from __future__ import annotations

import argparse
import logging
import random

from publishers.base_publisher import BasePublisher

logger = logging.getLogger(__name__)


class SoilMoistureSimulator(BasePublisher):
    sensor_type = "soil_moisture"
    unit = "%"
    topic_key = "soil_moisture"

    def __init__(self, device_id: str = "soil-001", field_id: str | None = None) -> None:
        super().__init__(device_id=device_id, field_id=field_id)
        self._current = random.uniform(35.0, 55.0)

    def generate_value(self) -> float:
        # Gunde yavas degisim + kucuk gurultu
        self._current += random.uniform(-1.5, 1.0)
        self._current = max(15.0, min(75.0, self._current))
        return round(self._current, 2)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Toprak nemi MQTT simulatörü")
    parser.add_argument("--field-id", default=None, help="Tarla ID")
    parser.add_argument("--device-id", default="soil-001", help="Cihaz ID")
    parser.add_argument("--interval", type=float, default=5.0, help="Yayin araligi (sn)")
    parser.add_argument("--count", type=int, default=None, help="Maksimum mesaj sayisi")
    args = parser.parse_args()

    simulator = SoilMoistureSimulator(device_id=args.device_id, field_id=args.field_id)
    simulator.run(interval_seconds=args.interval, max_messages=args.count)


if __name__ == "__main__":
    main()
