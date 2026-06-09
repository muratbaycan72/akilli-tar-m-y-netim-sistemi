import { useAppContext } from '../context/AppContext';
import { useFieldData, groupReadingsByType } from '../hooks/useFieldData';
import StatCard from '../components/dashboard/StatCard';
import SensorLineChart from '../components/charts/LineChart';
import SensorBarChart from '../components/charts/BarChart';

export default function Dashboard() {
  const { selectedField } = useAppContext();
  const { latest, readings, predictions, loading, error } = useFieldData(
    selectedField?.id ?? null,
  );

  if (!selectedField) {
    return (
      <div className="empty-state">
        <h3>Tarla Seçilmedi</h3>
        <p>Verileri görmek için üst menüden bir tarla seçin veya backend'de seed verisi oluşturun.</p>
      </div>
    );
  }

  if (loading) return <div className="loading">Veriler yükleniyor...</div>;

  const grouped = groupReadingsByType(readings);
  const soilReading = latest.find((r) => r.sensor_type === 'soil_moisture');
  const tempReading = latest.find((r) => r.sensor_type === 'temperature');
  const humidityReading = latest.find((r) => r.sensor_type === 'humidity');
  const lastPrediction = predictions.find((p) => p.prediction_type === 'soil_moisture');

  return (
    <>
      {error && <div className="error-banner">{error}</div>}

      <div className="stat-grid">
        <StatCard
          label="Toprak Nemi"
          value={soilReading?.value?.toFixed(1) ?? '—'}
          unit={soilReading?.unit ?? '%'}
          variant={soilReading && soilReading.value < 30 ? 'danger' : 'default'}
          subtitle={soilReading ? 'Son okuma' : 'Veri bekleniyor'}
        />
        <StatCard
          label="Sıcaklık"
          value={tempReading?.value?.toFixed(1) ?? '—'}
          unit={tempReading?.unit ?? '°C'}
          variant="info"
        />
        <StatCard
          label="Hava Nemi"
          value={humidityReading?.value?.toFixed(1) ?? '—'}
          unit={humidityReading?.unit ?? '%'}
        />
        <StatCard
          label="ML Tahmin (Toprak Nemi)"
          value={lastPrediction?.predicted_value?.toFixed(1) ?? '—'}
          unit="%"
          variant="warning"
          subtitle={
            lastPrediction?.confidence
              ? `Güven: ${(lastPrediction.confidence * 100).toFixed(0)}%`
              : 'Tahmin yapılmadı'
          }
        />
      </div>

      <div className="chart-grid">
        <SensorBarChart latestReadings={latest} />
        {Object.entries(grouped).slice(0, 2).map(([type, data]) => (
          <SensorLineChart key={type} readings={data} sensorType={type} />
        ))}
      </div>

      <div className="card">
        <h3 className="card-title">Tarla Bilgisi</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16 }}>
          <div><span className="stat-label">Ad</span><p style={{ fontWeight: 600 }}>{selectedField.name}</p></div>
          <div><span className="stat-label">Ürün</span><p style={{ fontWeight: 600 }}>{selectedField.crop_type || '—'}</p></div>
          <div><span className="stat-label">Konum</span><p style={{ fontWeight: 600 }}>{selectedField.location || '—'}</p></div>
          <div><span className="stat-label">Alan</span><p style={{ fontWeight: 600 }}>{selectedField.area_hectares ? `${selectedField.area_hectares} ha` : '—'}</p></div>
        </div>
      </div>
    </>
  );
}
