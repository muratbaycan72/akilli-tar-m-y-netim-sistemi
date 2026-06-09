export interface Field {
  id: string;
  user_id: string;
  name: string;
  location?: string;
  area_hectares?: number;
  crop_type?: string;
  latitude?: number;
  longitude?: number;
  is_active: boolean;
  created_at: string;
}

export interface Sensor {
  id: string;
  field_id: string;
  sensor_type: string;
  device_id: string;
  unit: string;
  is_active: boolean;
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
  input_features?: Record<string, number>;
  predicted_at: string;
}

export interface SoilMoisturePrediction {
  field_id: string;
  predicted_soil_moisture: number;
  unit: string;
  confidence: number;
  model_name: string;
  model_version: string;
  input_features: Record<string, number>;
  saved_prediction_id?: number;
}

export interface IrrigationLog {
  id: string;
  field_id: string;
  triggered_by: string;
  duration_minutes: number;
  water_amount_liters?: number;
  status: string;
  started_at: string;
  completed_at?: string;
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
  trained_at?: string;
}

export const SENSOR_LABELS: Record<string, string> = {
  soil_moisture: 'Toprak Nemi',
  temperature: 'Sıcaklık',
  humidity: 'Nem',
  light: 'Işık',
  ph: 'pH',
  plant_health: 'Bitki Sağlığı',
};

export const SENSOR_COLORS: Record<string, string> = {
  soil_moisture: '#2d6a4f',
  temperature: '#e76f51',
  humidity: '#457b9d',
  plant_health: '#52b788',
  light: '#f4a261',
  ph: '#9b5de5',
};
