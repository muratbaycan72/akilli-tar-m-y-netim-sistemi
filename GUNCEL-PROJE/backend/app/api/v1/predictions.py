"""ML tahmin ve alarm API endpoint'leri."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from psycopg2.extensions import connection as PgConnection

from app.core.exceptions import not_found
from app.db.crud import alert_crud, prediction_crud
from app.dependencies import get_db
from app.schemas import (
    AlertCreate,
    AlertResponse,
    MessageResponse,
    PredictionCreate,
    PredictionResponse,
    SoilMoisturePredictRequest,
    SoilMoisturePredictResponse,
)
from app.services.ml_inference_service import ml_service

predictions_router = APIRouter(prefix="/predictions", tags=["predictions"])
alerts_router = APIRouter(prefix="/alerts", tags=["alerts"])


@predictions_router.post("/soil-moisture", response_model=SoilMoisturePredictResponse)
def predict_soil_moisture(
    payload: SoilMoisturePredictRequest,
    save: bool = Query(default=True, description="Sonucu veritabanina kaydet"),
    conn: PgConnection = Depends(get_db),
):
    """TensorFlow Linear Regression modeli ile toprak nemi tahmini."""
    if not ml_service.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model yuklu degil. ml_models/src/training/train_regressor.py calistirin.",
        )

    features = {
        "temperature": payload.temperature,
        "humidity": payload.humidity,
        "rainfall_mm": payload.rainfall_mm,
        "wind_speed": payload.wind_speed,
        "solar_radiation": payload.solar_radiation,
    }

    result = ml_service.predict_soil_moisture(features)
    saved_id = None

    if save:
        row = prediction_crud.create_prediction(
            conn,
            field_id=payload.field_id,
            model_name=result["model_name"],
            model_version=result["model_version"],
            prediction_type="soil_moisture",
            predicted_value=result["predicted_value"],
            confidence=result["confidence"],
            input_features=result["input_features"],
        )
        saved_id = row["id"]

    return SoilMoisturePredictResponse(
        field_id=payload.field_id,
        predicted_soil_moisture=result["predicted_value"],
        confidence=result["confidence"],
        model_name=result["model_name"],
        model_version=result["model_version"],
        input_features=result["input_features"],
        saved_prediction_id=saved_id,
    )


@predictions_router.get("/model-info")
def get_model_info():
    """Yuklu ML model bilgilerini dondurur."""
    if not ml_service.is_ready:
        raise HTTPException(status_code=503, detail="ML model yuklu degil")
    meta = ml_service.metadata
    return {
        "model_name": meta["model_name"],
        "model_version": meta["model_version"],
        "features": meta["feature_names"],
        "metrics": meta.get("metrics"),
        "trained_at": meta.get("trained_at"),
    }


@predictions_router.post("", response_model=PredictionResponse, status_code=201)
def create_prediction(payload: PredictionCreate, conn: PgConnection = Depends(get_db)):
    row = prediction_crud.create_prediction(conn, **payload.model_dump())
    return row


@predictions_router.get("", response_model=list[PredictionResponse])
def list_predictions(
    field_id: str = Query(...),
    prediction_type: str | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    conn: PgConnection = Depends(get_db),
):
    return prediction_crud.get_predictions_by_field(conn, field_id, prediction_type, limit)


@predictions_router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: int, conn: PgConnection = Depends(get_db)):
    row = prediction_crud.get_prediction_by_id(conn, prediction_id)
    if not row:
        raise not_found("Tahmin", str(prediction_id))
    return row


@alerts_router.post("", response_model=AlertResponse, status_code=201)
def create_alert(payload: AlertCreate, conn: PgConnection = Depends(get_db)):
    row = alert_crud.create_alert(
        conn,
        field_id=payload.field_id,
        user_id=payload.user_id,
        alert_type=payload.alert_type,
        title=payload.title,
        message=payload.message,
        severity=payload.severity.value,
    )
    return row


@alerts_router.get("", response_model=list[AlertResponse])
def list_alerts(
    user_id: str = Query(...),
    unread_only: bool = Query(default=False),
    limit: int = Query(default=50, le=200),
    conn: PgConnection = Depends(get_db),
):
    return alert_crud.get_alerts_by_user(conn, user_id, unread_only, limit)


@alerts_router.patch("/{alert_id}/read", response_model=AlertResponse)
def mark_read(alert_id: str, conn: PgConnection = Depends(get_db)):
    row = alert_crud.mark_alert_read(conn, alert_id)
    if not row:
        raise not_found("Alarm", alert_id)
    return row


@alerts_router.delete("/{alert_id}", response_model=MessageResponse)
def delete_alert(alert_id: str, conn: PgConnection = Depends(get_db)):
    if not alert_crud.delete_alert(conn, alert_id):
        raise not_found("Alarm", alert_id)
    return MessageResponse(message="Alarm silindi")
