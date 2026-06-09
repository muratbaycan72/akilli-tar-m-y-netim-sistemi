import { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { useFieldData } from '../hooks/useFieldData';
import { api } from '../api/client';
import type { ModelInfo, SoilMoisturePrediction } from '../types';
import { useEffect } from 'react';

export default function Predictions() {
  const { selectedField } = useAppContext();
  const { latest, predictions, loading, error, refresh } = useFieldData(
    selectedField?.id ?? null,
  );

  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [livePrediction, setLivePrediction] = useState<SoilMoisturePrediction | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [predictError, setPredictError] = useState<string | null>(null);

  const [inputs, setInputs] = useState({
    temperature: 25,
    humidity: 60,
    rainfall_mm: 3,
    wind_speed: 10,
    solar_radiation: 500,
  });

  useEffect(() => {
    api.getModelInfo().then(setModelInfo).catch(() => {});
  }, []);

  useEffect(() => {
    const temp = latest.find((r) => r.sensor_type === 'temperature');
    const hum = latest.find((r) => r.sensor_type === 'humidity');
    if (temp) setInputs((p) => ({ ...p, temperature: temp.value }));
    if (hum) setInputs((p) => ({ ...p, humidity: hum.value }));
  }, [latest]);

  const handlePredict = async () => {
    if (!selectedField) return;
    setPredicting(true);
    setPredictError(null);
    try {
      const result = await api.predictSoilMoisture({
        field_id: selectedField.id,
        ...inputs,
      });
      setLivePrediction(result);
      refresh();
    } catch (e) {
      setPredictError(e instanceof Error ? e.message : 'Tahmin başarısız');
    } finally {
      setPredicting(false);
    }
  };

  if (!selectedField) {
    return (
      <div className="empty-state">
        <h3>Tarla Seçilmedi</h3>
        <p>Lütfen bir tarla seçin.</p>
      </div>
    );
  }

  if (loading) return <div className="loading">Tahminler yükleniyor...</div>;

  return (
    <>
      {error && <div className="error-banner">{error}</div>}

      {modelInfo && (
        <div className="stat-grid">
          <div className="stat-card info">
            <span className="stat-label">Model</span>
            <span className="stat-value" style={{ fontSize: 18 }}>
              {modelInfo.model_name} v{modelInfo.model_version}
            </span>
          </div>
          <div className="stat-card">
            <span className="stat-label">R² Skoru</span>
            <span className="stat-value">
              {modelInfo.metrics?.r2?.toFixed(3) ?? '—'}
            </span>
          </div>
          <div className="stat-card">
            <span className="stat-label">MAE</span>
            <span className="stat-value">
              {modelInfo.metrics?.mae?.toFixed(2) ?? '—'}
              <span className="stat-unit"> %</span>
            </span>
          </div>
        </div>
      )}

      <div className="control-panel" style={{ marginBottom: 28 }}>
        <div className="card">
          <h3 className="card-title">🧠 Toprak Nemi Tahmini</h3>
          {predictError && <div className="error-banner">{predictError}</div>}

          <div className="control-section">
            {(['temperature', 'humidity', 'rainfall_mm', 'wind_speed', 'solar_radiation'] as const).map(
              (key) => (
                <div className="form-group" key={key}>
                  <label>
                    {key === 'temperature' && 'Sıcaklık (°C)'}
                    {key === 'humidity' && 'Nem (%)'}
                    {key === 'rainfall_mm' && 'Yağış (mm)'}
                    {key === 'wind_speed' && 'Rüzgar (km/h)'}
                    {key === 'solar_radiation' && 'Güneş Radyasyonu (W/m²)'}
                  </label>
                  <input
                    type="number"
                    value={inputs[key]}
                    onChange={(e) =>
                      setInputs((p) => ({ ...p, [key]: Number(e.target.value) }))
                    }
                  />
                </div>
              ),
            )}
            <button
              className="btn btn-primary btn-lg"
              onClick={handlePredict}
              disabled={predicting}
            >
              {predicting ? 'Tahmin yapılıyor...' : '🔮 Tahmin Yap'}
            </button>
          </div>
        </div>

        <div className="card">
          <h3 className="card-title">Sonuç</h3>
          {livePrediction ? (
            <div style={{ textAlign: 'center', padding: '20px 0' }}>
              <div style={{ fontSize: 48, fontWeight: 700, color: 'var(--color-primary)' }}>
                {livePrediction.predicted_soil_moisture}
                <span style={{ fontSize: 20, color: 'var(--color-text-muted)' }}> %</span>
              </div>
              <p style={{ marginTop: 8, color: 'var(--color-text-muted)' }}>
                Güven: {(livePrediction.confidence * 100).toFixed(0)}%
              </p>
              <span className="badge badge-success" style={{ marginTop: 12 }}>
                {livePrediction.model_name} v{livePrediction.model_version}
              </span>
            </div>
          ) : (
            <div className="empty-state">
              <p>Tahmin yapmak için formu doldurup butona tıklayın.</p>
            </div>
          )}
        </div>
      </div>

      {predictions.length > 0 && (
        <div className="card">
          <h3 className="card-title">Geçmiş Tahminler</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Tarih</th>
                <th>Tahmin</th>
                <th>Güven</th>
                <th>Model</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((p) => (
                <tr key={p.id}>
                  <td>{new Date(p.predicted_at).toLocaleString('tr-TR')}</td>
                  <td><strong>{p.predicted_value.toFixed(1)}</strong> %</td>
                  <td>{p.confidence ? `${(p.confidence * 100).toFixed(0)}%` : '—'}</td>
                  <td>{p.model_name} v{p.model_version}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
