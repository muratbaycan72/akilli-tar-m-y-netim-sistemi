"""Tum sensör simulatörlerini tek komutla calistirir."""

from __future__ import annotations

import argparse
import logging
import threading
import time

from publishers.plant_health_simulator import PlantHealthSimulator
from publishers.soil_moisture_simulator import SoilMoistureSimulator
from publishers.weather_simulator import WeatherSimulator

logger = logging.getLogger(__name__)


def _run_in_thread(name: str, target, *args, **kwargs) -> threading.Thread:
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, name=name, daemon=True)
    thread.start()
    return thread


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Tum sensör simulatörlerini baslat")
    parser.add_argument("--field-id", default=None)
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--count", type=int, default=None)
    args = parser.parse_args()

    soil = SoilMoistureSimulator(field_id=args.field_id)
    weather = WeatherSimulator(field_id=args.field_id)
    plant = PlantHealthSimulator(field_id=args.field_id)

    threads = [
        _run_in_thread("soil", soil.run, args.interval, args.count),
        _run_in_thread("weather", weather.run, args.interval, args.count),
        _run_in_thread("plant", plant.run, args.interval * 2, args.count),
    ]

    logger.info("3 simulatör baslatildi. Durdurmak icin Ctrl+C.")
    try:
        while any(t.is_alive() for t in threads):
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Simulatörler durduruluyor...")


if __name__ == "__main__":
    main()
