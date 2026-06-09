"""Pydantic semalar."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SensorType(str, Enum):
    soil_moisture = "soil_moisture"
    temperature = "temperature"
    humidity = "humidity"
    light = "light"
    ph = "ph"
    plant_health = "plant_health"


class TriggerType(str, Enum):
    manual = "manual"
    automatic = "automatic"
    scheduled = "scheduled"


class AlertSeverity(str, Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(min_length=6)
    role: str = "farmer"


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class FieldCreate(BaseModel):
    user_id: str
    name: str
    location: str | None = None
    area_hectares: float | None = None
    crop_type: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class FieldUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    area_hectares: float | None = None
    crop_type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None


class FieldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    name: str
    location: str | None = None
    area_hectares: float | None = None
    crop_type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SensorCreate(BaseModel):
    field_id: str
    sensor_type: SensorType
    device_id: str
    unit: str


class SensorUpdate(BaseModel):
    sensor_type: SensorType | None = None
    unit: str | None = None
    is_active: bool | None = None


class SensorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    field_id: str
    sensor_type: str
    device_id: str
    unit: str
    is_active: bool
    installed_at: datetime
    created_at: datetime


class SensorReadingCreate(BaseModel):
    sensor_id: str
    field_id: str
    value: float
    unit: str
    recorded_at: datetime | None = None
    metadata: dict[str, Any] | None = None


class SensorReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: str
    field_id: str
    value: float
    unit: str
    recorded_at: datetime
    metadata: dict[str, Any] | None = None


class IrrigationCreate(BaseModel):
    field_id: str
    duration_minutes: int = Field(gt=0)
    triggered_by: TriggerType = TriggerType.manual
    water_amount_liters: float | None = None
    notes: str | None = None


class IrrigationStatusUpdate(BaseModel):
    status: str


class IrrigationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    field_id: str
    triggered_by: str
    duration_minutes: int
    water_amount_liters: float | None = None
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    notes: str | None = None


class FertilizationCreate(BaseModel):
    field_id: str
    fertilizer_type: str
    amount_kg: float = Field(gt=0)
    triggered_by: TriggerType = TriggerType.manual
    notes: str | None = None


class FertilizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    field_id: str
    fertilizer_type: str
    amount_kg: float
    triggered_by: str
    status: str
    applied_at: datetime
    notes: str | None = None


class SprayingCreate(BaseModel):
    field_id: str
    pesticide_type: str
    amount_liters: float = Field(gt=0)
    triggered_by: TriggerType = TriggerType.manual
    notes: str | None = None


class SprayingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    field_id: str
    pesticide_type: str
    amount_liters: float
    triggered_by: str
    status: str
    applied_at: datetime
    notes: str | None = None


class PredictionCreate(BaseModel):
    field_id: str
    model_name: str
    model_version: str
    prediction_type: str = "soil_moisture"
    predicted_value: float
    confidence: float | None = Field(default=None, ge=0, le=1)
    input_features: dict[str, Any] | None = None


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    field_id: str
    model_name: str
    model_version: str
    prediction_type: str
    predicted_value: float
    confidence: float | None = None
    input_features: dict[str, Any] | None = None
    predicted_at: datetime


class SoilMoisturePredictRequest(BaseModel):
    field_id: str
    temperature: float = Field(description="Hava sicakligi (C)")
    humidity: float = Field(ge=0, le=100, description="Hava nemi (%)")
    rainfall_mm: float = Field(default=0, ge=0, description="Son yagis (mm)")
    wind_speed: float = Field(default=0, ge=0, description="Ruzgar hizi (km/h)")
    solar_radiation: float = Field(default=400, ge=0, description="Gunes radyasyonu (W/m2)")


class SoilMoisturePredictResponse(BaseModel):
    field_id: str
    predicted_soil_moisture: float
    unit: str = "%"
    confidence: float
    model_name: str
    model_version: str
    input_features: dict[str, Any]
    saved_prediction_id: int | None = None


class AlertCreate(BaseModel):
    field_id: str
    user_id: str
    alert_type: str
    title: str
    message: str
    severity: AlertSeverity = AlertSeverity.warning


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    field_id: str
    user_id: str
    alert_type: str
    severity: str
    title: str
    message: str
    is_read: bool
    created_at: datetime


class MessageResponse(BaseModel):
    message: str
