"""Uygulama yapilandirmasi."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql://akilli_tarim:changeme_secure_password@localhost:5432/akilli_tarim_db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = True
    api_secret_key: str = "changeme_jwt_secret_key"

    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_topic_prefix: str = "akilli-tarim"

    ml_model_path: str = "../ml_models/saved_models/soil_moisture_v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
