"""MQTT subscriber istemcisi."""

from __future__ import annotations

import logging
from typing import Any, Callable

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from utils.config_loader import MqttConfig, TopicConfig, load_mqtt_config, load_topic_config

logger = logging.getLogger(__name__)

MessageHandler = Callable[[str, bytes], None]


class MqttSubscriber:
    """Sensör topic'lerini dinleyen MQTT istemcisi."""

    def __init__(
        self,
        on_message_callback: MessageHandler | None = None,
        mqtt_config: MqttConfig | None = None,
        topic_config: TopicConfig | None = None,
        subscribe_topic: str | None = None,
    ) -> None:
        self.mqtt_config = mqtt_config or load_mqtt_config()
        self.topic_config = topic_config or load_topic_config()
        self.subscribe_topic = subscribe_topic or self.topic_config.sensor_wildcard()
        self._on_message_callback = on_message_callback
        self._client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=f"{self.mqtt_config.client_id}_subscriber",
        )
        if self.mqtt_config.username and self.mqtt_config.password:
            self._client.username_pw_set(self.mqtt_config.username, self.mqtt_config.password)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: Any,
        reason_code: mqtt.ReasonCode,
        properties: Any = None,
    ) -> None:
        if reason_code == 0:
            client.subscribe(self.subscribe_topic, qos=self.mqtt_config.qos)
            logger.info("Dinleniyor: %s", self.subscribe_topic)
        else:
            logger.error("Baglanti basarisiz, reason_code=%s", reason_code)

    def _on_message(
        self,
        client: mqtt.Client,
        userdata: Any,
        msg: mqtt.MQTTMessage,
    ) -> None:
        if self._on_message_callback:
            self._on_message_callback(msg.topic, msg.payload)
        else:
            logger.info("Mesaj alindi | topic=%s | payload=%s", msg.topic, msg.payload.decode("utf-8"))

    def start(self) -> None:
        self._client.connect(
            self.mqtt_config.broker_host,
            self.mqtt_config.broker_port,
            self.mqtt_config.keepalive,
        )
        logger.info("Subscriber baslatildi (%s:%s)", self.mqtt_config.broker_host, self.mqtt_config.broker_port)
        self._client.loop_forever()

    def stop(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()
