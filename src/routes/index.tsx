import { createFileRoute } from '@tanstack/react-router';
import { getLatestSensorData } from '../lib/sensors.functions';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const Route = createFileRoute('/')({
  loader: async () => await getLatestSensorData(),
  component: Dashboard,
});

function Dashboard() {
  const data = Route.useLoaderData();
  if (data.source !== 'db') return <div>Veri yükleniyor veya hata oluştu...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>AgriMind Panel</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ padding: '1rem', background: '#f3f4f6', borderRadius: '8px' }}>
          <h3>Sıcaklık: {data.latest?.temp}°C</h3>
        </div>
        <div style={{ padding: '1rem', background: '#f3f4f6', borderRadius: '8px' }}>
          <h3>Nem: {data.latest?.hum}%</h3>
        </div>
      </div>
      <div style={{ height: '300px', width: '100%' }}>
        <ResponsiveContainer>
          <LineChart data={data.series}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="t" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="temp" stroke="#ef4444" name="Sıcaklık" />
            <Line type="monotone" dataKey="hum" stroke="#3b82f6" name="Nem" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}