"""MQTT mesajlarini PostgreSQL'e kaydeden kopru servisi."""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from app.config import get_settings
from app.db.connection import get_connection
from app.db.crud import sensor_crud, sensor_reading_crud

logger = logging.getLogger(__name__)


class MqttBridge:
    """IoT MQTT verilerini sensor_readings tablosuna yazar."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id="akilli_tarim_backend_bridge",
        )
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._thread: threading.Thread | None = None

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: Any,
        reason_code: mqtt.ReasonCode,
        properties: Any = None,
    ) -> None:
        if reason_code == 0:
            topic = f"{self.settings.mqtt_topic_prefix}/+/sensors/#"
            client.subscribe(topic, qos=1)
            logger.info("MQTT bridge dinleniyor: %s", topic)

    def _on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            device_id = payload.get("device_id")
            field_id = payload.get("field_id")
            value = payload.get("value")
            unit = payload.get("unit")

            if not all([device_id, field_id, value is not None, unit]):
                logger.warning("Eksik MQTT payload: %s", payload)
                return

            with get_connection() as conn:
                sensor = sensor_crud.get_sensor_by_device_id(conn, device_id)
                if not sensor:
                    sensor_type = payload.get("sensor_type", "soil_moisture")
                    sensor = sensor_crud.create_sensor(conn, field_id, sensor_type, device_id, unit)

                recorded_at = None
                if payload.get("timestamp"):
                    recorded_at = datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))

                sensor_reading_crud.create_reading(
                    conn,
                    sensor_id=sensor["id"],
                    field_id=field_id,
                    value=float(value),
                    unit=unit,
                    recorded_at=recorded_at,
                    metadata=payload.get("metadata"),
                )
            logger.info("MQTT -> DB | device=%s value=%s %s", device_id, value, unit)
        except Exception as exc:
            logger.error("MQTT bridge hatasi: %s", exc)

    def start_background(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def _run() -> None:
            try:
                self._client.connect(self.settings.mqtt_broker_host, self.settings.mqtt_broker_port, 60)
                self._client.loop_forever()
            except Exception as exc:
                logger.warning("MQTT bridge baslatilamadi: %s", exc)

        self._thread = threading.Thread(target=_run, name="mqtt-bridge", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()
