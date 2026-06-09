import type {
  Alert,
  Field,
  IrrigationLog,
  MLPrediction,
  ModelInfo,
  SensorReading,
  SoilMoisturePrediction,
} from '../types';

const BASE_URL =
  process.env.EXPO_PUBLIC_API_URL || 'http://10.0.2.2:8000/api/v1';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(typeof err.detail === 'string' ? err.detail : `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  getFields: () => request<Field[]>('/fields'),

  getLatestReadings: (fieldId: string) =>
    request<SensorReading[]>(`/sensors/readings/latest?field_id=${fieldId}`),

  getReadingsByField: (fieldId: string, limit = 50) =>
    request<SensorReading[]>(`/sensors/readings/field/${fieldId}?limit=${limit}`),

  getPredictions: (fieldId: string) =>
    request<MLPrediction[]>(`/predictions?field_id=${fieldId}`),

  predictSoilMoisture: (data: {
    field_id: string;
    temperature: number;
    humidity: number;
    rainfall_mm?: number;
    wind_speed?: number;
    solar_radiation?: number;
  }) =>
    request<SoilMoisturePrediction>('/predictions/soil-moisture', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getModelInfo: () => request<ModelInfo>('/predictions/model-info'),

  startIrrigation: (data: {
    field_id: string;
    duration_minutes: number;
    water_amount_liters?: number;
    notes?: string;
  }) =>
    request<IrrigationLog>('/irrigation', {
      method: 'POST',
      body: JSON.stringify({ ...data, triggered_by: 'manual' }),
    }),

  getIrrigationLogs: (fieldId: string) =>
    request<IrrigationLog[]>(`/irrigation?field_id=${fieldId}`),

  getAlerts: (userId: string) =>
    request<Alert[]>(`/alerts?user_id=${userId}`),
};

export { BASE_URL };
