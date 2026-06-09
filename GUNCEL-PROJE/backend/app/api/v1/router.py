"""API v1 router birlestirici."""

from fastapi import APIRouter

from app.api.v1 import auth, fields, operations, predictions, sensors

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(fields.router)
api_router.include_router(sensors.router)
api_router.include_router(operations.router)
api_router.include_router(predictions.predictions_router)
api_router.include_router(predictions.alerts_router)
