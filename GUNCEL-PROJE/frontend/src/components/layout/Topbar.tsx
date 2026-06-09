import { useEffect } from 'react';
import { useAppContext } from '../../context/AppContext';
import { useFields } from '../../hooks/useFieldData';

interface TopbarProps {
  title: string;
}

export default function Topbar({ title }: TopbarProps) {
  const { fields, loading } = useFields();
  const { selectedField, setSelectedField } = useAppContext();

  useEffect(() => {
    if (!selectedField && fields.length > 0) {
      setSelectedField(fields[0]);
    }
  }, [fields, selectedField, setSelectedField]);

  return (
    <header className="topbar">
      <h2 className="topbar-title">{title}</h2>
      <div className="topbar-actions">
        <select
          className="field-select"
          value={selectedField?.id || ''}
          onChange={(e) => {
            const field = fields.find((f) => f.id === e.target.value);
            setSelectedField(field || null);
          }}
          disabled={loading}
        >
          {fields.length === 0 && <option value="">Tarla seçin...</option>}
          {fields.map((f) => (
            <option key={f.id} value={f.id}>
              {f.name} {f.crop_type ? `(${f.crop_type})` : ''}
            </option>
          ))}
        </select>
      </div>
    </header>
  );
}
