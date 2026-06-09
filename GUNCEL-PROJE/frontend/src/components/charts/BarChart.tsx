import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { SENSOR_COLORS, SENSOR_LABELS, type SensorReading } from '../../types';

interface SensorBarChartProps {
  latestReadings: SensorReading[];
  title?: string;
}

export default function SensorBarChart({ latestReadings, title = 'Anlık Sensör Değerleri' }: SensorBarChartProps) {
  const data = latestReadings.map((r) => ({
    name: SENSOR_LABELS[r.sensor_type || ''] || r.sensor_type || 'Bilinmeyen',
    value: r.value,
    fill: SENSOR_COLORS[r.sensor_type || ''] || '#2d6a4f',
  }));

  if (data.length === 0) {
    return (
      <div className="card">
        <h3 className="card-title">{title}</h3>
        <div className="empty-state"><p>Henüz veri yok</p></div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="card-title">{title}</h3>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid #e5e7eb' }} />
            <Bar dataKey="value" radius={[6, 6, 0, 0]}>
              {data.map((entry, i) => (
                <Cell key={i} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
