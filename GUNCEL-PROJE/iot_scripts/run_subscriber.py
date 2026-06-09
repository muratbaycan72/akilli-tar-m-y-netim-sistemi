"""MQTT subscriber CLI giris noktasi."""

from __future__ import annotations

import argparse
import logging

from subscribers.data_ingestion_handler import DataIngestionHandler
from subscribers.mqtt_client import MqttSubscriber

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Sensör verilerini MQTT uzerinden dinle")
    parser.add_argument("--topic", default=None, help="Dinlenecek topic (varsayilan: wildcard)")
    args = parser.parse_args()

    handler = DataIngestionHandler()
    subscriber = MqttSubscriber(
        on_message_callback=handler.create_callback(),
        subscribe_topic=args.topic,
    )

    try:
        subscriber.start()
    except KeyboardInterrupt:
        logger.info("Subscriber durduruldu.")
        logger.info("Ozet: %s", handler.stats.summary())


if __name__ == "__main__":
    main()
