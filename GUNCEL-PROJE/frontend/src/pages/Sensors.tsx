import { useAppContext } from '../context/AppContext';
import { useFieldData, groupReadingsByType } from '../hooks/useFieldData';
import SensorLineChart from '../components/charts/LineChart';

export default function Sensors() {
  const { selectedField } = useAppContext();
  const { readings, latest, loading, error } = useFieldData(selectedField?.id ?? null);

  if (!selectedField) {
    return (
      <div className="empty-state">
        <h3>Tarla Seçilmedi</h3>
        <p>Lütfen bir tarla seçin.</p>
      </div>
    );
  }

  if (loading) return <div className="loading">Sensör verileri yükleniyor...</div>;

  const grouped = groupReadingsByType(readings);

  return (
    <>
      {error && <div className="error-banner">{error}</div>}

      <div className="chart-grid">
        {Object.keys(grouped).length > 0 ? (
          Object.entries(grouped).map(([type, data]) => (
            <SensorLineChart key={type} readings={data} sensorType={type} />
          ))
        ) : (
          <div className="card">
            <div className="empty-state">
              <h3>Henüz sensör verisi yok</h3>
              <p>IoT simülatörlerini çalıştırarak veri gönderebilirsiniz.</p>
            </div>
          </div>
        )}
      </div>

      {latest.length > 0 && (
        <div className="card">
          <h3 className="card-title">Son Okumalar</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Sensör</th>
                <th>Değer</th>
                <th>Cihaz</th>
                <th>Zaman</th>
              </tr>
            </thead>
            <tbody>
              {latest.map((r) => (
                <tr key={r.id}>
                  <td>{r.sensor_type || '—'}</td>
                  <td><strong>{r.value}</strong> {r.unit}</td>
                  <td>{r.device_id || '—'}</td>
                  <td>{new Date(r.recorded_at).toLocaleString('tr-TR')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
