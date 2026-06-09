"""Tarla CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute, execute_returning, fetch_all, fetch_one


def create_field(conn: PgConnection, user_id: str, name: str, **kwargs) -> dict:
    data = {
        "user_id": user_id,
        "name": name,
        "location": kwargs.get("location"),
        "area_hectares": kwargs.get("area_hectares"),
        "crop_type": kwargs.get("crop_type"),
        "latitude": kwargs.get("latitude"),
        "longitude": kwargs.get("longitude"),
    }
    return execute_returning(
        conn,
        """
        INSERT INTO fields (user_id, name, location, area_hectares, crop_type, latitude, longitude)
        VALUES (%(user_id)s, %(name)s, %(location)s, %(area_hectares)s, %(crop_type)s, %(latitude)s, %(longitude)s)
        RETURNING *
        """,
        data,
    )


def get_field_by_id(conn: PgConnection, field_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM fields WHERE id = %s", (field_id,))


def get_fields_by_user(conn: PgConnection, user_id: str) -> list[dict]:
    return fetch_all(conn, "SELECT * FROM fields WHERE user_id = %s ORDER BY created_at DESC", (user_id,))


def get_all_fields(conn: PgConnection, limit: int = 50, offset: int = 0) -> list[dict]:
    return fetch_all(conn, "SELECT * FROM fields ORDER BY created_at DESC LIMIT %s OFFSET %s", (limit, offset))


def update_field(conn: PgConnection, field_id: str, **fields) -> dict | None:
    allowed = {"name", "location", "area_hectares", "crop_type", "latitude", "longitude", "is_active"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return get_field_by_id(conn, field_id)
    set_clause = ", ".join(f"{k} = %({k})s" for k in updates)
    updates["field_id"] = field_id
    return execute_returning(
        conn,
        f"UPDATE fields SET {set_clause} WHERE id = %(field_id)s RETURNING *",
        updates,
    )


def delete_field(conn: PgConnection, field_id: str) -> bool:
    return execute(conn, "DELETE FROM fields WHERE id = %s", (field_id,)) > 0
