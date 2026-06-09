"""MQTT ve sensör topic yapilandirmasini yukler."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"

load_dotenv(ROOT_DIR.parent / ".env")


@dataclass(frozen=True)
class MqttConfig:
    broker_host: str
    broker_port: int
    client_id: str
    keepalive: int
    qos: int
    username: str | None = None
    password: str | None = None
    topic_prefix: str = "akilli-tarim"


@dataclass(frozen=True)
class TopicConfig:
    prefix: str
    templates: dict[str, str]
    default_field_id: str

    def build_topic(self, sensor_key: str, field_id: str | None = None) -> str:
        field = field_id or self.default_field_id
        template = self.templates[sensor_key]
        return template.format(prefix=self.prefix, field_id=field)

    def sensor_wildcard(self) -> str:
        return f"{self.prefix}/+/sensors/#"


def load_mqtt_config() -> MqttConfig:
    with open(CONFIG_DIR / "mqtt_config.yaml", encoding="utf-8") as file:
        raw = yaml.safe_load(file)["mqtt"]

    with open(CONFIG_DIR / "sensor_topics.yaml", encoding="utf-8") as file:
        topics_raw = yaml.safe_load(file)

    return MqttConfig(
        broker_host=os.getenv("MQTT_BROKER_HOST", raw["broker_host"]),
        broker_port=int(os.getenv("MQTT_BROKER_PORT", raw["broker_port"])),
        client_id=os.getenv("MQTT_CLIENT_ID", raw["client_id"]),
        keepalive=int(raw["keepalive"]),
        qos=int(raw["qos"]),
        username=os.getenv("MQTT_USERNAME") or None,
        password=os.getenv("MQTT_PASSWORD") or None,
        topic_prefix=os.getenv("MQTT_TOPIC_PREFIX", topics_raw["topic_prefix"]),
    )


def load_topic_config() -> TopicConfig:
    with open(CONFIG_DIR / "sensor_topics.yaml", encoding="utf-8") as file:
        raw = yaml.safe_load(file)

    prefix = os.getenv("MQTT_TOPIC_PREFIX", raw["topic_prefix"])
    return TopicConfig(
        prefix=prefix,
        templates=raw["topics"],
        default_field_id=raw["default_field_id"],
    )
