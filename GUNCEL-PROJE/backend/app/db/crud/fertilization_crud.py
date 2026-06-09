"""Gubreleme kayit CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute_returning, fetch_all, fetch_one


def create_fertilization_log(
    conn: PgConnection,
    field_id: str,
    fertilizer_type: str,
    amount_kg: float,
    **kwargs,
) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO fertilization_logs
            (field_id, fertilizer_type, amount_kg, triggered_by, status, notes)
        VALUES
            (%(field_id)s, %(fertilizer_type)s, %(amount_kg)s,
             %(triggered_by)s, %(status)s, %(notes)s)
        RETURNING *
        """,
        {
            "field_id": field_id,
            "fertilizer_type": fertilizer_type,
            "amount_kg": amount_kg,
            "triggered_by": kwargs.get("triggered_by", "manual"),
            "status": kwargs.get("status", "completed"),
            "notes": kwargs.get("notes"),
        },
    )


def get_fertilization_by_field(conn: PgConnection, field_id: str, limit: int = 50) -> list[dict]:
    return fetch_all(
        conn,
        "SELECT * FROM fertilization_logs WHERE field_id = %s ORDER BY applied_at DESC LIMIT %s",
        (field_id, limit),
    )


def get_fertilization_by_id(conn: PgConnection, log_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM fertilization_logs WHERE id = %s", (log_id,))
