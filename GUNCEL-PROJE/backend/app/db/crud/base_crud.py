"""CRUD yardimci fonksiyonlari."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor, Json


def row_to_dict(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    result: dict[str, Any] = {}
    for key, value in dict(row).items():
        if isinstance(value, UUID):
            result[key] = str(value)
        else:
            result[key] = value
    return result


def rows_to_list(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row_to_dict(row) for row in rows]  # type: ignore[misc]


def fetch_one(conn: PgConnection, query: str, params: tuple | dict | None = None) -> dict[str, Any] | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return row_to_dict(cur.fetchone())


def fetch_all(conn: PgConnection, query: str, params: tuple | dict | None = None) -> list[dict[str, Any]]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return rows_to_list(cur.fetchall())


def execute_returning(conn: PgConnection, query: str, params: tuple | dict | None = None) -> dict[str, Any] | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return row_to_dict(cur.fetchone())


def execute(conn: PgConnection, query: str, params: tuple | dict | None = None) -> int:
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.rowcount


def to_json(value: dict | None) -> Json:
    return Json(value or {})
