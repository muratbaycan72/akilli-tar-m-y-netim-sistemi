import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Sensors from './pages/Sensors';
import Predictions from './pages/Predictions';
import Operations from './pages/Operations';
import Alerts from './pages/Alerts';

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="sensors" element={<Sensors />} />
            <Route path="predictions" element={<Predictions />} />
            <Route path="operations" element={<Operations />} />
            <Route path="alerts" element={<Alerts />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}
