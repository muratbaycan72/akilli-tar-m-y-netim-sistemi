"""Hava durumu sensör simulatörü (sicaklik + nem)."""

from __future__ import annotations

import argparse
import logging
import random
import time
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from utils.config_loader import load_mqtt_config, load_topic_config
from utils.payload import build_sensor_payload, serialize_payload

logger = logging.getLogger(__name__)


class WeatherSimulator:
    """Sicaklik ve nem verilerini ayri topic'lere yayinlar."""

    def __init__(self, device_id: str = "weather-001", field_id: str | None = None) -> None:
        self.device_id = device_id
        self.mqtt_config = load_mqtt_config()
        self.topic_config = load_topic_config()
        self.field_id = field_id or self.topic_config.default_field_id
        self._temperature = random.uniform(18.0, 28.0)
        self._humidity = random.uniform(45.0, 70.0)
        self._client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=f"{self.mqtt_config.client_id}_{device_id}",
        )
        if self.mqtt_config.username and self.mqtt_config.password:
            self._client.username_pw_set(self.mqtt_config.username, self.mqtt_config.password)

    def connect(self) -> None:
        self._client.connect(
            self.mqtt_config.broker_host,
            self.mqtt_config.broker_port,
            self.mqtt_config.keepalive,
        )
        self._client.loop_start()

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def _next_temperature(self) -> float:
        self._temperature += random.uniform(-0.8, 0.8)
        self._temperature = max(5.0, min(40.0, self._temperature))
        return round(self._temperature, 2)

    def _next_humidity(self) -> float:
        self._humidity += random.uniform(-2.0, 2.0)
        self._humidity = max(20.0, min(95.0, self._humidity))
        return round(self._humidity, 2)

    def _publish(self, topic_key: str, sensor_type: str, value: float, unit: str) -> dict[str, Any]:
        topic = self.topic_config.build_topic(topic_key, self.field_id)
        payload = build_sensor_payload(
            device_id=self.device_id,
            field_id=self.field_id,
            sensor_type=sensor_type,
            value=value,
            unit=unit,
            metadata={"simulator": True, "bundle": "weather"},
        )
        result = self._client.publish(topic, serialize_payload(payload), qos=self.mqtt_config.qos)
        result.wait_for_publish(timeout=5)
        logger.info("Yayinlandi -> %s | value=%s %s", topic, value, unit)
        return payload

    def publish_once(self) -> list[dict[str, Any]]:
        return [
            self._publish("temperature", "temperature", self._next_temperature(), "C"),
            self._publish("humidity", "humidity", self._next_humidity(), "%"),
        ]

    def run(self, interval_seconds: float = 5.0, max_cycles: int | None = None) -> None:
        self.connect()
        cycles = 0
        try:
            while max_cycles is None or cycles < max_cycles:
                self.publish_once()
                cycles += 1
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Durduruldu (KeyboardInterrupt)")
        finally:
            self.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Hava durumu MQTT simulatörü")
    parser.add_argument("--field-id", default=None)
    parser.add_argument("--device-id", default="weather-001")
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--count", type=int, default=None)
    args = parser.parse_args()

    simulator = WeatherSimulator(device_id=args.device_id, field_id=args.field_id)
    simulator.run(interval_seconds=args.interval, max_cycles=args.count)


if __name__ == "__main__":
    main()
