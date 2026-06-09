"""Kullanici CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute_returning, fetch_all, fetch_one


def create_user(conn: PgConnection, email: str, full_name: str, password_hash: str, role: str = "farmer") -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO users (email, full_name, password_hash, role)
        VALUES (%(email)s, %(full_name)s, %(password_hash)s, %(role)s)
        RETURNING id, email, full_name, role, is_active, created_at, updated_at
        """,
        {"email": email, "full_name": full_name, "password_hash": password_hash, "role": role},
    )


def get_user_by_id(conn: PgConnection, user_id: str) -> dict | None:
    return fetch_one(
        conn,
        "SELECT id, email, full_name, role, is_active, created_at, updated_at FROM users WHERE id = %s",
        (user_id,),
    )


def get_user_by_email(conn: PgConnection, email: str) -> dict | None:
    return fetch_one(conn, "SELECT * FROM users WHERE email = %s", (email,))


def get_all_users(conn: PgConnection, limit: int = 50, offset: int = 0) -> list[dict]:
    return fetch_all(
        conn,
        """
        SELECT id, email, full_name, role, is_active, created_at, updated_at
        FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s
        """,
        (limit, offset),
    )


def update_user(conn: PgConnection, user_id: str, **fields) -> dict | None:
    allowed = {"full_name", "role", "is_active"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not updates:
        return get_user_by_id(conn, user_id)
    set_clause = ", ".join(f"{k} = %({k})s" for k in updates)
    updates["user_id"] = user_id
    return execute_returning(
        conn,
        f"""
        UPDATE users SET {set_clause}
        WHERE id = %(user_id)s
        RETURNING id, email, full_name, role, is_active, created_at, updated_at
        """,
        updates,
    )


def delete_user(conn: PgConnection, user_id: str) -> bool:
    from app.db.crud.base_crud import execute

    return execute(conn, "DELETE FROM users WHERE id = %s", (user_id,)) > 0
