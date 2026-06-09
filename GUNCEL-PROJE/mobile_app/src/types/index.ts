export interface Field {
  id: string;
  user_id: string;
  name: string;
  location?: string;
  area_hectares?: number;
  crop_type?: string;
  is_active: boolean;
  created_at: string;
}

export interface SensorReading {
  id: number;
  sensor_id: string;
  field_id: string;
  value: number;
  unit: string;
  recorded_at: string;
  sensor_type?: string;
  device_id?: string;
}

export interface MLPrediction {
  id: number;
  field_id: string;
  model_name: string;
  model_version: string;
  prediction_type: string;
  predicted_value: number;
  confidence?: number;
  predicted_at: string;
}

export interface SoilMoisturePrediction {
  field_id: string;
  predicted_soil_moisture: number;
  unit: string;
  confidence: number;
  model_name: string;
  model_version: string;
}

export interface IrrigationLog {
  id: string;
  field_id: string;
  triggered_by: string;
  duration_minutes: number;
  water_amount_liters?: number;
  status: string;
  started_at: string;
  notes?: string;
}

export interface Alert {
  id: string;
  field_id: string;
  user_id: string;
  alert_type: string;
  severity: 'info' | 'warning' | 'critical';
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface ModelInfo {
  model_name: string;
  model_version: string;
  features: string[];
  metrics?: { mae: number; rmse: number; r2: number };
}
