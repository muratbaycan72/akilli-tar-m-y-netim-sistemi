import { NavLink } from 'react-router-dom';

const links = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/sensors', label: 'Sensörler', icon: '📡' },
  { to: '/predictions', label: 'ML Tahminler', icon: '🧠' },
  { to: '/operations', label: 'Kontrol Paneli', icon: '🎛️' },
  { to: '/alerts', label: 'Alarmlar', icon: '🔔' },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <img src="/leaf.svg" alt="Logo" />
        <div>
          <h1>Akıllı Tarım</h1>
          <span>Yönetim Sistemi</span>
        </div>
      </div>
      <nav className="sidebar-nav">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === '/'}
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
