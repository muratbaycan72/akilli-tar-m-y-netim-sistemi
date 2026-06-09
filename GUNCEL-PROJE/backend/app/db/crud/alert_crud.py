"""Alarm CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute, execute_returning, fetch_all, fetch_one


def create_alert(
    conn: PgConnection,
    field_id: str,
    user_id: str,
    alert_type: str,
    title: str,
    message: str,
    severity: str = "warning",
) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO alerts (field_id, user_id, alert_type, severity, title, message)
        VALUES (%(field_id)s, %(user_id)s, %(alert_type)s, %(severity)s, %(title)s, %(message)s)
        RETURNING *
        """,
        {
            "field_id": field_id,
            "user_id": user_id,
            "alert_type": alert_type,
            "severity": severity,
            "title": title,
            "message": message,
        },
    )


def get_alert_by_id(conn: PgConnection, alert_id: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM alerts WHERE id = %s", (alert_id,))


def get_alerts_by_user(conn: PgConnection, user_id: str, unread_only: bool = False, limit: int = 50) -> list[dict]:
    if unread_only:
        return fetch_all(
            conn,
            "SELECT * FROM alerts WHERE user_id = %s AND is_read = FALSE ORDER BY created_at DESC LIMIT %s",
            (user_id, limit),
        )
    return fetch_all(
        conn,
        "SELECT * FROM alerts WHERE user_id = %s ORDER BY created_at DESC LIMIT %s",
        (user_id, limit),
    )


def mark_alert_read(conn: PgConnection, alert_id: str) -> dict | None:
    return execute_returning(
        conn,
        "UPDATE alerts SET is_read = TRUE WHERE id = %s RETURNING *",
        (alert_id,),
    )


def delete_alert(conn: PgConnection, alert_id: str) -> bool:
    return execute(conn, "DELETE FROM alerts WHERE id = %s", (alert_id,)) > 0
