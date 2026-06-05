import { createFileRoute } from '@tanstack/react-router';
import { getLatestSensorData } from '../../lib/sensors.functions';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const Route = createFileRoute('/')({
  loader: async () => await getLatestSensorData(),
  component: Dashboard,
});

function Dashboard() {
  const data = Route.useLoaderData();

  if (data.source === 'error') return <div>Veri çekme hatası!</div>;
  if (data.source === 'empty') return <div>Veri yok.</div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>AgriMind Panel</h1>
      {/* Basit bir kart */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div style={{ border: '1px solid #ccc', padding: '10px' }}>
          <h3>Sıcaklık</h3>
          <p>{data.latest?.temp}°C</p>
        </div>
      </div>
      
      {/* Grafik */}
      <div style={{ height: '300px', width: '100%' }}>
        <ResponsiveContainer>
          <LineChart data={data.series}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="t" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="temp" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}