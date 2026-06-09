import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { SENSOR_COLORS, SENSOR_LABELS, type SensorReading } from '../../types';
import { formatTime } from '../../hooks/useFieldData';

interface SensorLineChartProps {
  readings: SensorReading[];
  sensorType: string;
  title?: string;
}

export default function SensorLineChart({ readings, sensorType, title }: SensorLineChartProps) {
  const data = readings.map((r) => ({
    time: formatTime(r.recorded_at),
    value: r.value,
  }));

  const color = SENSOR_COLORS[sensorType] || '#2d6a4f';
  const label = title || SENSOR_LABELS[sensorType] || sensorType;

  if (data.length === 0) {
    return (
      <div className="card">
        <h3 className="card-title">{label}</h3>
        <div className="empty-state">
          <p>Henüz veri yok</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="card-title">{label}</h3>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="time" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip
              contentStyle={{ borderRadius: 8, border: '1px solid #e5e7eb' }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="value"
              name={label}
              stroke={color}
              strokeWidth={2}
              dot={{ r: 3, fill: color }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
