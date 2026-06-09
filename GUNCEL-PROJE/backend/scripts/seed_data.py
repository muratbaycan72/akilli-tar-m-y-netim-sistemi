"""Ornek veri olusturma scripti."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.connection import get_connection, init_pool
from app.db.crud import field_crud, sensor_crud, user_crud


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed() -> None:
    init_pool()
    with get_connection() as conn:
        existing = user_crud.get_user_by_email(conn, "demo@tarim.com")
        if existing:
            user_id = existing["id"]
            print(f"Mevcut kullanici kullaniliyor: {user_id}")
        else:
            user = user_crud.create_user(
                conn,
                email="demo@tarim.com",
                full_name="Demo Ciftci",
                password_hash=hash_password("demo123"),
                role="farmer",
            )
            user_id = user["id"]
            print(f"Kullanici olusturuldu: {user_id}")

        fields = field_crud.get_fields_by_user(conn, user_id)
        if fields:
            field_id = fields[0]["id"]
            print(f"Mevcut tarla kullaniliyor: {field_id}")
        else:
            field = field_crud.create_field(
                conn,
                user_id=user_id,
                name="Ana Tarla",
                location="Konya, Türkiye",
                area_hectares=12.5,
                crop_type="bugday",
                latitude=37.8746,
                longitude=32.4932,
            )
            field_id = field["id"]
            print(f"Tarla olusturuldu: {field_id}")

        sensors = [
            ("soil-001", "soil_moisture", "%"),
            ("weather-001", "temperature", "C"),
            ("weather-001-h", "humidity", "%"),
            ("plant-001", "plant_health", "score"),
        ]
        for device_id, sensor_type, unit in sensors:
            if sensor_crud.get_sensor_by_device_id(conn, device_id):
                print(f"  Sensör mevcut: {device_id}")
                continue
            sensor = sensor_crud.create_sensor(conn, field_id, sensor_type, device_id, unit)
            print(f"  Sensör olusturuldu: {sensor['id']} ({device_id})")

    print("\nSeed tamamlandi.")
    print("  E-posta: demo@tarim.com")
    print("  Sifre:   demo123")


if __name__ == "__main__":
    seed()
