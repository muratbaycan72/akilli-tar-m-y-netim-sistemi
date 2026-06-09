"""Sensör okuma CRUD islemleri."""

from __future__ import annotations

from datetime import datetime

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute_returning, fetch_all, fetch_one, to_json


def create_reading(
    conn: PgConnection,
    sensor_id: str,
    field_id: str,
    value: float,
    unit: str,
    recorded_at: datetime | None = None,
    metadata: dict | None = None,
) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO sensor_readings (sensor_id, field_id, value, unit, recorded_at, metadata)
        VALUES (%(sensor_id)s, %(field_id)s, %(value)s, %(unit)s,
                COALESCE(%(recorded_at)s, NOW()), %(metadata)s)
        RETURNING *
        """,
        {
            "sensor_id": sensor_id,
            "field_id": field_id,
            "value": value,
            "unit": unit,
            "recorded_at": recorded_at,
            "metadata": to_json(metadata),
        },
    )


def get_reading_by_id(conn: PgConnection, reading_id: int) -> dict | None:
    return fetch_one(conn, "SELECT * FROM sensor_readings WHERE id = %s", (reading_id,))


def get_readings_by_sensor(
    conn: PgConnection,
    sensor_id: str,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    return fetch_all(
        conn,
        """
        SELECT * FROM sensor_readings
        WHERE sensor_id = %s
        ORDER BY recorded_at DESC
        LIMIT %s OFFSET %s
        """,
        (sensor_id, limit, offset),
    )


def get_readings_by_field(
    conn: PgConnection,
    field_id: str,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    return fetch_all(
        conn,
        """
        SELECT * FROM sensor_readings
        WHERE field_id = %s
        ORDER BY recorded_at DESC
        LIMIT %s OFFSET %s
        """,
        (field_id, limit, offset),
    )


def get_latest_readings_by_field(conn: PgConnection, field_id: str) -> list[dict]:
    return fetch_all(
        conn,
        """
        SELECT DISTINCT ON (s.sensor_type)
            sr.*, s.sensor_type, s.device_id
        FROM sensor_readings sr
        JOIN sensors s ON s.id = sr.sensor_id
        WHERE sr.field_id = %s
        ORDER BY s.sensor_type, sr.recorded_at DESC
        """,
        (field_id,),
    )
