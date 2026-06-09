"""FastAPI bagimliliklari."""

from __future__ import annotations

from typing import Generator

from psycopg2.extensions import connection as PgConnection

from app.db.connection import get_db as _get_db


def get_db() -> Generator[PgConnection, None, None]:
    yield from _get_db()
