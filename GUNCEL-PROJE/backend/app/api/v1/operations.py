"""Operasyon API endpoint'leri (sulama, gubreleme, ilaclama)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection as PgConnection

from app.core.exceptions import not_found
from app.db.crud import fertilization_crud, irrigation_crud, spraying_crud
from app.dependencies import get_db
from app.schemas import (
    FertilizationCreate,
    FertilizationResponse,
    IrrigationCreate,
    IrrigationResponse,
    IrrigationStatusUpdate,
    SprayingCreate,
    SprayingResponse,
)

router = APIRouter(tags=["operations"])


@router.post("/irrigation", response_model=IrrigationResponse, status_code=201)
def start_irrigation(payload: IrrigationCreate, conn: PgConnection = Depends(get_db)):
    row = irrigation_crud.create_irrigation_log(
        conn,
        field_id=payload.field_id,
        duration_minutes=payload.duration_minutes,
        triggered_by=payload.triggered_by.value,
        water_amount_liters=payload.water_amount_liters,
        notes=payload.notes,
        status="running",
    )
    return row


@router.get("/irrigation", response_model=list[IrrigationResponse])
def list_irrigation(
    field_id: str = Query(...),
    limit: int = Query(default=50, le=200),
    conn: PgConnection = Depends(get_db),
):
    return irrigation_crud.get_irrigation_by_field(conn, field_id, limit)


@router.patch("/irrigation/{log_id}", response_model=IrrigationResponse)
def update_irrigation(log_id: str, payload: IrrigationStatusUpdate, conn: PgConnection = Depends(get_db)):
    row = irrigation_crud.update_irrigation_status(conn, log_id, payload.status)
    if not row:
        raise not_found("Sulama kaydi", log_id)
    return row


@router.post("/fertilization", response_model=FertilizationResponse, status_code=201)
def create_fertilization(payload: FertilizationCreate, conn: PgConnection = Depends(get_db)):
    row = fertilization_crud.create_fertilization_log(
        conn,
        field_id=payload.field_id,
        fertilizer_type=payload.fertilizer_type,
        amount_kg=payload.amount_kg,
        triggered_by=payload.triggered_by.value,
        notes=payload.notes,
    )
    return row


@router.get("/fertilization", response_model=list[FertilizationResponse])
def list_fertilization(
    field_id: str = Query(...),
    limit: int = Query(default=50, le=200),
    conn: PgConnection = Depends(get_db),
):
    return fertilization_crud.get_fertilization_by_field(conn, field_id, limit)


@router.post("/spraying", response_model=SprayingResponse, status_code=201)
def create_spraying(payload: SprayingCreate, conn: PgConnection = Depends(get_db)):
    row = spraying_crud.create_spraying_log(
        conn,
        field_id=payload.field_id,
        pesticide_type=payload.pesticide_type,
        amount_liters=payload.amount_liters,
        triggered_by=payload.triggered_by.value,
        notes=payload.notes,
    )
    return row


@router.get("/spraying", response_model=list[SprayingResponse])
def list_spraying(
    field_id: str = Query(...),
    limit: int = Query(default=50, le=200),
    conn: PgConnection = Depends(get_db),
):
    return spraying_crud.get_spraying_by_field(conn, field_id, limit)
