"""Sensör API endpoint'leri."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection as PgConnection

from app.core.exceptions import not_found
from app.db.crud import sensor_crud, sensor_reading_crud
from app.dependencies import get_db
from app.schemas import (
    SensorCreate,
    SensorReadingCreate,
    SensorReadingResponse,
    SensorResponse,
    SensorUpdate,
    MessageResponse,
)

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.post("", response_model=SensorResponse, status_code=201)
def create_sensor(payload: SensorCreate, conn: PgConnection = Depends(get_db)):
    row = sensor_crud.create_sensor(
        conn,
        field_id=payload.field_id,
        sensor_type=payload.sensor_type.value,
        device_id=payload.device_id,
        unit=payload.unit,
    )
    return row


@router.get("", response_model=list[SensorResponse])
def list_sensors(
    field_id: str | None = Query(default=None),
    limit: int = Query(default=100, le=500),
    conn: PgConnection = Depends(get_db),
):
    if field_id:
        return sensor_crud.get_sensors_by_field(conn, field_id)
    return sensor_crud.get_all_sensors(conn, limit)


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: str, conn: PgConnection = Depends(get_db)):
    row = sensor_crud.get_sensor_by_id(conn, sensor_id)
    if not row:
        raise not_found("Sensör", sensor_id)
    return row


@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: str, payload: SensorUpdate, conn: PgConnection = Depends(get_db)):
    if not sensor_crud.get_sensor_by_id(conn, sensor_id):
        raise not_found("Sensör", sensor_id)
    data = payload.model_dump(exclude_unset=True)
    if "sensor_type" in data and data["sensor_type"] is not None:
        data["sensor_type"] = data["sensor_type"].value
    row = sensor_crud.update_sensor(conn, sensor_id, **data)
    return row


@router.delete("/{sensor_id}", response_model=MessageResponse)
def delete_sensor(sensor_id: str, conn: PgConnection = Depends(get_db)):
    if not sensor_crud.delete_sensor(conn, sensor_id):
        raise not_found("Sensör", sensor_id)
    return MessageResponse(message="Sensör silindi")


@router.post("/readings", response_model=SensorReadingResponse, status_code=201)
def create_reading(payload: SensorReadingCreate, conn: PgConnection = Depends(get_db)):
    row = sensor_reading_crud.create_reading(conn, **payload.model_dump())
    return row


@router.get("/readings/latest", response_model=list[SensorReadingResponse])
def latest_readings(field_id: str = Query(...), conn: PgConnection = Depends(get_db)):
    return sensor_reading_crud.get_latest_readings_by_field(conn, field_id)


@router.get("/readings/field/{field_id}", response_model=list[SensorReadingResponse])
def readings_by_field(
    field_id: str,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
    conn: PgConnection = Depends(get_db),
):
    return sensor_reading_crud.get_readings_by_field(conn, field_id, limit, offset)


@router.get("/readings/sensor/{sensor_id}", response_model=list[SensorReadingResponse])
def readings_by_sensor(
    sensor_id: str,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
    conn: PgConnection = Depends(get_db),
):
    return sensor_reading_crud.get_readings_by_sensor(conn, sensor_id, limit, offset)
