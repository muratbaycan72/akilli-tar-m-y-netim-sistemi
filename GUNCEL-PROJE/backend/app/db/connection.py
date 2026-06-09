"""PostgreSQL baglanti havuzu (psycopg2)."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2 import pool
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor

from app.config import get_settings

logger = logging.getLogger(__name__)

_connection_pool: pool.SimpleConnectionPool | None = None
_pool_available: bool = False


def init_pool(minconn: int = 1, maxconn: int = 10) -> bool:
    global _connection_pool, _pool_available
    if _connection_pool is not None:
        return _pool_available
    try:
        settings = get_settings()
        _connection_pool = pool.SimpleConnectionPool(
            minconn,
            maxconn,
            settings.database_url,
            cursor_factory=RealDictCursor,
        )
        _pool_available = True
        return True
    except psycopg2.Error as exc:
        logger.warning("Veritabani havuzu baslatilamadi: %s", exc)
        _pool_available = False
        return False


def close_pool() -> None:
    global _connection_pool, _pool_available
    if _connection_pool is not None:
        _connection_pool.closeall()
        _connection_pool = None
    _pool_available = False


@contextmanager
def get_connection() -> Generator[PgConnection, None, None]:
    if _connection_pool is None:
        init_pool()
    if _connection_pool is None or not _pool_available:
        raise psycopg2.OperationalError("Veritabani baglantisi kullanilamiyor")
    conn = _connection_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _connection_pool.putconn(conn)


def get_db() -> Generator[PgConnection, None, None]:
    """FastAPI dependency."""
    with get_connection() as conn:
        yield conn
