import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

const PAGE_TITLES: Record<string, string> = {
  '/': 'Dashboard',
  '/sensors': 'Sensör Verileri',
  '/predictions': 'ML Tahminler',
  '/operations': 'Kontrol Paneli',
  '/alerts': 'Alarmlar',
};

export default function Layout() {
  const path = window.location.pathname;
  const title = PAGE_TITLES[path] || 'Dashboard';

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Topbar title={title} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
