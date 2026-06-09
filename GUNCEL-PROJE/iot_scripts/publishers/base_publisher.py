"""MQTT tabanli sensör veri yayinci sinifi."""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from utils.config_loader import MqttConfig, TopicConfig, load_mqtt_config, load_topic_config
from utils.payload import build_sensor_payload, serialize_payload

logger = logging.getLogger(__name__)


class BasePublisher(ABC):
    """Sensör simulatörleri icin ortak MQTT publisher."""

    sensor_type: str
    unit: str
    topic_key: str

    def __init__(
        self,
        device_id: str,
        field_id: str | None = None,
        mqtt_config: MqttConfig | None = None,
        topic_config: TopicConfig | None = None,
    ) -> None:
        self.device_id = device_id
        self.field_id = field_id or (topic_config or load_topic_config()).default_field_id
        self.mqtt_config = mqtt_config or load_mqtt_config()
        self.topic_config = topic_config or load_topic_config()
        self._client = self._create_client()

    def _create_client(self) -> mqtt.Client:
        client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=f"{self.mqtt_config.client_id}_{self.device_id}",
        )
        if self.mqtt_config.username and self.mqtt_config.password:
            client.username_pw_set(self.mqtt_config.username, self.mqtt_config.password)
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        return client

    @staticmethod
    def _on_connect(
        client: mqtt.Client,
        userdata: Any,
        flags: Any,
        reason_code: mqtt.ReasonCode,
        properties: Any = None,
    ) -> None:
        if reason_code == 0:
            logger.info("Broker'a baglandi")
        else:
            logger.error("Baglanti basarisiz, reason_code=%s", reason_code)

    @staticmethod
    def _on_disconnect(
        client: mqtt.Client,
        userdata: Any,
        flags: Any,
        reason_code: mqtt.ReasonCode,
        properties: Any = None,
    ) -> None:
        logger.info("Broker baglantisi kesildi (reason_code=%s)", reason_code)

    @abstractmethod
    def generate_value(self) -> float:
        """Bir sonraki olcum degerini uret."""

    def build_payload(self) -> dict[str, Any]:
        return build_sensor_payload(
            device_id=self.device_id,
            field_id=self.field_id,
            sensor_type=self.sensor_type,
            value=self.generate_value(),
            unit=self.unit,
            metadata={"simulator": True, "device_id": self.device_id},
        )

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

    def publish_once(self) -> dict[str, Any]:
        topic = self.topic_config.build_topic(self.topic_key, self.field_id)
        payload = self.build_payload()
        message = serialize_payload(payload)
        result = self._client.publish(topic, message, qos=self.mqtt_config.qos)
        result.wait_for_publish(timeout=5)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"Yayin basarisiz (rc={result.rc}) topic={topic}")
        logger.info("Yayinlandi -> %s | value=%s %s", topic, payload["value"], self.unit)
        return payload

    def run(self, interval_seconds: float = 5.0, max_messages: int | None = None) -> None:
        self.connect()
        sent = 0
        try:
            while max_messages is None or sent < max_messages:
                self.publish_once()
                sent += 1
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Durduruldu (KeyboardInterrupt)")
        finally:
            self.disconnect()
