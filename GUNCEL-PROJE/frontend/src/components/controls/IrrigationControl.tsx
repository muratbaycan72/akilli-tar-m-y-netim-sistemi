import { useState } from 'react';
import { api } from '../../api/client';
import { useAppContext } from '../../context/AppContext';

interface IrrigationControlProps {
  onSuccess?: () => void;
}

export default function IrrigationControl({ onSuccess }: IrrigationControlProps) {
  const { selectedField } = useAppContext();
  const [duration, setDuration] = useState(30);
  const [waterAmount, setWaterAmount] = useState(500);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleStart = async () => {
    if (!selectedField) return;
    setLoading(true);
    setMessage(null);
    try {
      await api.startIrrigation({
        field_id: selectedField.id,
        duration_minutes: duration,
        water_amount_liters: waterAmount,
        notes: 'Web dashboard üzerinden manuel tetiklendi',
      });
      setMessage({ type: 'success', text: `Sulama başlatıldı (${duration} dk, ${waterAmount} L)` });
      onSuccess?.();
    } catch (e) {
      setMessage({
        type: 'error',
        text: e instanceof Error ? e.message : 'Sulama başlatılamadı',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3 className="card-title">💧 Sulama Kontrolü</h3>

      {message && (
        <div className={message.type === 'success' ? 'success-banner' : 'error-banner'}>
          {message.text}
        </div>
      )}

      <div className="control-section">
        <div className="form-row">
          <div className="form-group" style={{ flex: 1 }}>
            <label>Süre (dakika)</label>
            <input
              type="number"
              min={1}
              max={180}
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
            />
          </div>
          <div className="form-group" style={{ flex: 1 }}>
            <label>Su Miktarı (litre)</label>
            <input
              type="number"
              min={1}
              value={waterAmount}
              onChange={(e) => setWaterAmount(Number(e.target.value))}
            />
          </div>
        </div>

        <button
          className="btn btn-primary btn-lg"
          onClick={handleStart}
          disabled={loading || !selectedField}
        >
          {loading ? 'Başlatılıyor...' : '🚿 Sulamayı Başlat'}
        </button>

        {!selectedField && (
          <p style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>
            Lütfen üst menüden bir tarla seçin.
          </p>
        )}
      </div>
    </div>
  );
}
