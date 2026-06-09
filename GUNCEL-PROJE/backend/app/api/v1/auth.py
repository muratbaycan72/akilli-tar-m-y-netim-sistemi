"""Kullanici API endpoint'leri."""

from __future__ import annotations

import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.extensions import connection as PgConnection

from app.core.exceptions import not_found
from app.db.crud import user_crud
from app.dependencies import get_db
from app.schemas import MessageResponse, UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, conn: PgConnection = Depends(get_db)):
    if user_crud.get_user_by_email(conn, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-posta zaten kayitli")
    row = user_crud.create_user(
        conn,
        email=payload.email,
        full_name=payload.full_name,
        password_hash=_hash_password(payload.password),
        role=payload.role,
    )
    return row


@router.get("", response_model=list[UserResponse])
def list_users(
    limit: int = 50,
    offset: int = 0,
    conn: PgConnection = Depends(get_db),
):
    return user_crud.get_all_users(conn, limit, offset)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, conn: PgConnection = Depends(get_db)):
    row = user_crud.get_user_by_id(conn, user_id)
    if not row:
        raise not_found("Kullanici", user_id)
    return row


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, payload: UserUpdate, conn: PgConnection = Depends(get_db)):
    if not user_crud.get_user_by_id(conn, user_id):
        raise not_found("Kullanici", user_id)
    row = user_crud.update_user(conn, user_id, **payload.model_dump(exclude_unset=True))
    return row


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: str, conn: PgConnection = Depends(get_db)):
    if not user_crud.delete_user(conn, user_id):
        raise not_found("Kullanici", user_id)
    return MessageResponse(message="Kullanici silindi")
