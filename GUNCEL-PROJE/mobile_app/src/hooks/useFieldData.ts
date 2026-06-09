import { useCallback, useEffect, useState } from 'react';
import { AppState, type AppStateStatus } from 'react-native';
import { api } from '../services/api';
import type { Alert, IrrigationLog, MLPrediction, SensorReading } from '../types';

const POLL_MS = 30_000;

export function useFieldData(fieldId: string | null) {
  const [latest, setLatest] = useState<SensorReading[]>([]);
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [predictions, setPredictions] = useState<MLPrediction[]>([]);
  const [irrigationLogs, setIrrigationLogs] = useState<IrrigationLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!fieldId) return;
    try {
      setError(null);
      const [l, r, p, i] = await Promise.all([
        api.getLatestReadings(fieldId),
        api.getReadingsByField(fieldId, 50),
        api.getPredictions(fieldId),
        api.getIrrigationLogs(fieldId),
      ]);
      setLatest(l);
      setReadings(r);
      setPredictions(p);
      setIrrigationLogs(i);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Veri yüklenemedi');
    } finally {
      setLoading(false);
    }
  }, [fieldId]);

  useEffect(() => {
    setLoading(true);
    refresh();
    const timer = setInterval(refresh, POLL_MS);
    return () => clearInterval(timer);
  }, [refresh]);

  useEffect(() => {
    const sub = AppState.addEventListener('change', (state: AppStateStatus) => {
      if (state === 'active') refresh();
    });
    return () => sub.remove();
  }, [refresh]);

  return { latest, readings, predictions, irrigationLogs, loading, error, refresh };
}

export function useAlerts(userId: string | null) {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const refresh = useCallback(async () => {
    if (!userId) return;
    try {
      setAlerts(await api.getAlerts(userId));
    } catch {
      /* ignore */
    }
  }, [userId]);

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, POLL_MS);
    return () => clearInterval(timer);
  }, [refresh]);

  return { alerts, refresh };
}

export function formatTime(iso: string): string {
  return new Date(iso).toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function groupBySensorType(readings: SensorReading[]) {
  const groups: Record<string, SensorReading[]> = {};
  for (const r of readings) {
    const t = r.sensor_type || 'unknown';
    if (!groups[t]) groups[t] = [];
    groups[t].push(r);
  }
  for (const k of Object.keys(groups)) {
    groups[k].sort(
      (a, b) => new Date(a.recorded_at).getTime() - new Date(b.recorded_at).getTime(),
    );
  }
  return groups;
}
