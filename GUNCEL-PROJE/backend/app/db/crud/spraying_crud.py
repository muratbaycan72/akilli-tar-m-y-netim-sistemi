"""Ilaclama kayit CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute_returning, fetch_all, fetch_one


def create_spraying_log(
    conn: PgConnection,
    field_id: str,
    pesticide_type: str,
    amount_liters: float,
    **kwargs,
) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO spraying_logs
            (field_id, pesticide_type, amount_liters, triggered_by, status, notes)
        VALUES
            (%(field_id)s, %(pesticide_type)s, %(amount_liters)s,
             %(triggered_by)s, %(status)s, %(notes)s)
        RETURNING *
        """,
        {
            "field_id": field_id,
            "pesticide_type": pesticide_type,
            "amount_liters": amount_liters,
            "triggered_by": kwargs.get("triggered_by", "manual"),
            "status": kwargs.get("status", "completed"),
            "notes": kwargs.get("notes"),
        },
    )


def get_spraying_by_field(conn: PgConnection, field_id: str, limit: int = 50) -> list[dict]:
    return fetch_all(
        conn,
        "SELECT * FROM spraying_logs WHERE field_id = %s ORDER BY applied_at DESC LIMIT %s",
        (field_id, limit),
    )


def get_spraying_by_id(conn: PgConnection, log_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM spraying_logs WHERE id = %s", (log_id,))
