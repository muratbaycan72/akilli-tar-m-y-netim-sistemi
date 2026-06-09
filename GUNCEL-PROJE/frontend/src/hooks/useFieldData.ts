import { useCallback, useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Alert, Field, IrrigationLog, MLPrediction, SensorReading } from '../types';

const POLL_INTERVAL = 30_000;

export function useFieldData(fieldId: string | null) {
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [latest, setLatest] = useState<SensorReading[]>([]);
  const [predictions, setPredictions] = useState<MLPrediction[]>([]);
  const [irrigationLogs, setIrrigationLogs] = useState<IrrigationLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!fieldId) return;
    try {
      setError(null);
      const [r, l, p, i] = await Promise.all([
        api.getReadingsByField(fieldId, 50),
        api.getLatestReadings(fieldId),
        api.getPredictions(fieldId),
        api.getIrrigationLogs(fieldId),
      ]);
      setReadings(r);
      setLatest(l);
      setPredictions(p);
      setIrrigationLogs(i);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Veri yüklenemedi');
    } finally {
      setLoading(false);
    }
  }, [fieldId]);

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, POLL_INTERVAL);
    return () => clearInterval(timer);
  }, [refresh]);

  return { readings, latest, predictions, irrigationLogs, loading, error, refresh };
}

export function useFields() {
  const [fields, setFields] = useState<Field[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getFields()
      .then(setFields)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return { fields, loading, error };
}

export function useAlerts(userId: string | null) {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    if (!userId) return;
    api.getAlerts(userId).then(setAlerts).catch(() => {});
  }, [userId]);

  return alerts;
}

export function formatTime(iso: string): string {
  return new Date(iso).toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function groupReadingsByType(readings: SensorReading[]) {
  const groups: Record<string, SensorReading[]> = {};
  for (const r of readings) {
    const type = r.sensor_type || 'unknown';
    if (!groups[type]) groups[type] = [];
    groups[type].push(r);
  }
  for (const key of Object.keys(groups)) {
    groups[key].sort(
      (a, b) => new Date(a.recorded_at).getTime() - new Date(b.recorded_at).getTime(),
    );
  }
  return groups;
}
