export interface SensorReading {
  device_id: string;
  field_id: string;
  sensor_type: string;
  value: number;
  unit: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface MLPrediction {
  field_id: string;
  model_name: string;
  model_version: string;
  prediction_type: string;
  predicted_value: number;
  confidence?: number;
  predicted_at: string;
}

export interface Alert {
  id: string;
  field_id: string;
  alert_type: string;
  severity: 'info' | 'warning' | 'critical';
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface Field {
  id: string;
  name: string;
  location?: string;
  crop_type?: string;
  area_hectares?: number;
  is_active: boolean;
}
