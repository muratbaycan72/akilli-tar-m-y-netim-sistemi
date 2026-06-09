import { useAppContext } from '../context/AppContext';
import { useAlerts } from '../hooks/useFieldData';

export default function Alerts() {
  const { selectedField } = useAppContext();
  const alerts = useAlerts(selectedField?.user_id ?? null);

  const filtered = selectedField
    ? alerts.filter((a) => a.field_id === selectedField.id)
    : alerts;

  return (
    <>
      <div className="card">
        <h3 className="card-title">🔔 Bildirimler</h3>
        {filtered.length === 0 ? (
          <div className="empty-state">
            <h3>Alarm yok</h3>
            <p>Tüm sistemler normal çalışıyor.</p>
          </div>
        ) : (
          <div className="alert-list">
            {filtered.map((alert) => (
              <div key={alert.id} className={`alert-item ${alert.severity}`}>
                <h4>{alert.title}</h4>
                <p>{alert.message}</p>
                <p style={{ fontSize: 11, marginTop: 8, opacity: 0.7 }}>
                  {new Date(alert.created_at).toLocaleString('tr-TR')}
                  {!alert.is_read && ' · Okunmadı'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
