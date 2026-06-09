"""Tarla API endpoint'leri."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection as PgConnection

from app.core.exceptions import not_found
from app.db.crud import field_crud
from app.dependencies import get_db
from app.schemas import FieldCreate, FieldResponse, FieldUpdate, MessageResponse

router = APIRouter(prefix="/fields", tags=["fields"])


@router.post("", response_model=FieldResponse, status_code=201)
def create_field(payload: FieldCreate, conn: PgConnection = Depends(get_db)):
    row = field_crud.create_field(conn, **payload.model_dump())
    return row


@router.get("", response_model=list[FieldResponse])
def list_fields(
    user_id: str | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    conn: PgConnection = Depends(get_db),
):
    if user_id:
        return field_crud.get_fields_by_user(conn, user_id)
    return field_crud.get_all_fields(conn, limit, offset)


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(field_id: str, conn: PgConnection = Depends(get_db)):
    row = field_crud.get_field_by_id(conn, field_id)
    if not row:
        raise not_found("Tarla", field_id)
    return row


@router.put("/{field_id}", response_model=FieldResponse)
def update_field(field_id: str, payload: FieldUpdate, conn: PgConnection = Depends(get_db)):
    if not field_crud.get_field_by_id(conn, field_id):
        raise not_found("Tarla", field_id)
    row = field_crud.update_field(conn, field_id, **payload.model_dump(exclude_unset=True))
    return row


@router.delete("/{field_id}", response_model=MessageResponse)
def delete_field(field_id: str, conn: PgConnection = Depends(get_db)):
    if not field_crud.delete_field(conn, field_id):
        raise not_found("Tarla", field_id)
    return MessageResponse(message="Tarla silindi")
