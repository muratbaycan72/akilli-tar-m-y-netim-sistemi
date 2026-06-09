const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  getFields: (userId?: string) =>
    request<import('../types').Field[]>(userId ? `/fields?user_id=${userId}` : '/fields'),

  getField: (id: string) => request<import('../types').Field>(`/fields/${id}`),

  getSensors: (fieldId: string) =>
    request<import('../types').Sensor[]>(`/sensors?field_id=${fieldId}`),

  getReadingsByField: (fieldId: string, limit = 100) =>
    request<import('../types').SensorReading[]>(
      `/sensors/readings/field/${fieldId}?limit=${limit}`,
    ),

  getLatestReadings: (fieldId: string) =>
    request<import('../types').SensorReading[]>(
      `/sensors/readings/latest?field_id=${fieldId}`,
    ),

  getPredictions: (fieldId: string) =>
    request<import('../types').MLPrediction[]>(`/predictions?field_id=${fieldId}`),

  predictSoilMoisture: (data: {
    field_id: string;
    temperature: number;
    humidity: number;
    rainfall_mm?: number;
    wind_speed?: number;
    solar_radiation?: number;
  }) =>
    request<import('../types').SoilMoisturePrediction>('/predictions/soil-moisture', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getModelInfo: () => request<import('../types').ModelInfo>('/predictions/model-info'),

  startIrrigation: (data: {
    field_id: string;
    duration_minutes: number;
    water_amount_liters?: number;
    notes?: string;
  }) =>
    request<import('../types').IrrigationLog>('/irrigation', {
      method: 'POST',
      body: JSON.stringify({ ...data, triggered_by: 'manual' }),
    }),

  getIrrigationLogs: (fieldId: string) =>
    request<import('../types').IrrigationLog[]>(`/irrigation?field_id=${fieldId}`),

  getAlerts: (userId: string) =>
    request<import('../types').Alert[]>(`/alerts?user_id=${userId}`),
};
