"""Sensör CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute, execute_returning, fetch_all, fetch_one


def create_sensor(
    conn: PgConnection,
    field_id: str,
    sensor_type: str,
    device_id: str,
    unit: str,
) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO sensors (field_id, sensor_type, device_id, unit)
        VALUES (%(field_id)s, %(sensor_type)s, %(device_id)s, %(unit)s)
        RETURNING *
        """,
        {"field_id": field_id, "sensor_type": sensor_type, "device_id": device_id, "unit": unit},
    )


def get_sensor_by_id(conn: PgConnection, sensor_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM sensors WHERE id = %s", (sensor_id,))


def get_sensor_by_device_id(conn: PgConnection, device_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM sensors WHERE device_id = %s", (device_id,))


def get_sensors_by_field(conn: PgConnection, field_id: str) -> list[dict]:
    return fetch_all(conn, "SELECT * FROM sensors WHERE field_id = %s ORDER BY created_at DESC", (field_id,))


def get_all_sensors(conn: PgConnection, limit: int = 100) -> list[dict]:
    return fetch_all(conn, "SELECT * FROM sensors ORDER BY created_at DESC LIMIT %s", (limit,))


def update_sensor(conn: PgConnection, sensor_id: str, **fields) -> dict | None:
    allowed = {"sensor_type", "unit", "is_active"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return get_sensor_by_id(conn, sensor_id)
    set_clause = ", ".join(f"{k} = %({k})s" for k in updates)
    updates["sensor_id"] = sensor_id
    return execute_returning(
        conn,
        f"UPDATE sensors SET {set_clause} WHERE id = %(sensor_id)s RETURNING *",
        updates,
    )


def delete_sensor(conn: PgConnection, sensor_id: str) -> bool:
    return execute(conn, "DELETE FROM sensors WHERE id = %s", (sensor_id,)) > 0
