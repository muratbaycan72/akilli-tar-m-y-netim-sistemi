"""Sulama kayit CRUD islemleri."""

from __future__ import annotations

from datetime import datetime

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute_returning, fetch_all, fetch_one


def create_irrigation_log(conn: PgConnection, field_id: str, duration_minutes: int, **kwargs) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO irrigation_logs
            (field_id, triggered_by, duration_minutes, water_amount_liters, status, notes)
        VALUES
            (%(field_id)s, %(triggered_by)s, %(duration_minutes)s,
             %(water_amount_liters)s, %(status)s, %(notes)s)
        RETURNING *
        """,
        {
            "field_id": field_id,
            "triggered_by": kwargs.get("triggered_by", "manual"),
            "duration_minutes": duration_minutes,
            "water_amount_liters": kwargs.get("water_amount_liters"),
            "status": kwargs.get("status", "pending"),
            "notes": kwargs.get("notes"),
        },
    )


def get_irrigation_by_id(conn: PgConnection, log_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM irrigation_logs WHERE id = %s", (log_id,))


def get_irrigation_by_field(conn: PgConnection, field_id: str, limit: int = 50) -> list[dict]:
    return fetch_all(
        conn,
        "SELECT * FROM irrigation_logs WHERE field_id = %s ORDER BY started_at DESC LIMIT %s",
        (field_id, limit),
    )


def update_irrigation_status(
    conn: PgConnection,
    log_id: str,
    status: str,
    completed_at: datetime | None = None,
) -> dict | None:
    return execute_returning(
        conn,
        """
        UPDATE irrigation_logs
        SET status = %(status)s,
            completed_at = COALESCE(%(completed_at)s, CASE WHEN %(status)s = 'completed' THEN NOW() ELSE completed_at END)
        WHERE id = %(log_id)s
        RETURNING *
        """,
        {"log_id": log_id, "status": status, "completed_at": completed_at},
    )
