import { useAppContext } from '../context/AppContext';
import { useFieldData, formatTime } from '../hooks/useFieldData';
import IrrigationControl from '../components/controls/IrrigationControl';

export default function Operations() {
  const { selectedField } = useAppContext();
  const { irrigationLogs, loading, error, refresh } = useFieldData(
    selectedField?.id ?? null,
  );

  if (!selectedField) {
    return (
      <div className="empty-state">
        <h3>Tarla Seçilmedi</h3>
        <p>Lütfen bir tarla seçin.</p>
      </div>
    );
  }

  if (loading) return <div className="loading">Yükleniyor...</div>;

  const statusBadge = (status: string) => {
    const map: Record<string, string> = {
      completed: 'badge-success',
      running: 'badge-info',
      pending: 'badge-warning',
      failed: 'badge-danger',
      cancelled: 'badge-warning',
    };
    return map[status] || 'badge-info';
  };

  return (
    <>
      {error && <div className="error-banner">{error}</div>}

      <div className="control-panel" style={{ marginBottom: 28 }}>
        <IrrigationControl onSuccess={refresh} />

        <div className="card">
          <h3 className="card-title">📋 Hızlı Bilgi</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div>
              <span className="stat-label">Seçili Tarla</span>
              <p style={{ fontWeight: 600, fontSize: 18 }}>{selectedField.name}</p>
            </div>
            <div>
              <span className="stat-label">Toplam Sulama</span>
              <p style={{ fontWeight: 600, fontSize: 18 }}>{irrigationLogs.length} kayıt</p>
            </div>
            <div>
              <span className="stat-label">Son Sulama</span>
              <p style={{ fontWeight: 600 }}>
                {irrigationLogs[0]
                  ? formatTime(irrigationLogs[0].started_at)
                  : 'Henüz sulama yapılmadı'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="card-title">Sulama Geçmişi</h3>
        {irrigationLogs.length === 0 ? (
          <div className="empty-state">
            <p>Henüz sulama kaydı yok.</p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Tarih</th>
                <th>Süre</th>
                <th>Su (L)</th>
                <th>Tetikleyici</th>
                <th>Durum</th>
              </tr>
            </thead>
            <tbody>
              {irrigationLogs.map((log) => (
                <tr key={log.id}>
                  <td>{formatTime(log.started_at)}</td>
                  <td>{log.duration_minutes} dk</td>
                  <td>{log.water_amount_liters ?? '—'}</td>
                  <td>{log.triggered_by}</td>
                  <td>
                    <span className={`badge ${statusBadge(log.status)}`}>
                      {log.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
