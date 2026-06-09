"""FastAPI uygulama giris noktasi."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import get_settings
from app.db.connection import close_pool, init_pool
from app.services.mqtt_bridge import MqttBridge

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

mqtt_bridge = MqttBridge()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if init_pool():
        logger.info("Veritabani havuzu baslatildi")
    else:
        logger.warning("Veritabani yok - API sinirli modda calisiyor")
    try:
        mqtt_bridge.start_background()
    except Exception as exc:
        logger.warning("MQTT bridge devre disi: %s", exc)
    yield
    mqtt_bridge.stop()
    close_pool()
    logger.info("Uygulama kapatildi")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Akilli Tarim Yonetim Sistemi API",
        description="Sensör verileri, operasyonlar ve ML tahminleri icin REST API",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.api_debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health_check():
        return {"status": "ok", "service": "akilli-tarim-api"}

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
