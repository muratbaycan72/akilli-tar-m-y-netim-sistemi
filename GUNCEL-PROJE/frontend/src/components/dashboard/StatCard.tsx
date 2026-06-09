interface StatCardProps {
  label: string;
  value: string | number;
  unit?: string;
  variant?: 'default' | 'warning' | 'danger' | 'info';
  subtitle?: string;
}

export default function StatCard({ label, value, unit, variant = 'default', subtitle }: StatCardProps) {
  return (
    <div className={`stat-card ${variant !== 'default' ? variant : ''}`}>
      <span className="stat-label">{label}</span>
      <span className="stat-value">
        {value}
        {unit && <span className="stat-unit"> {unit}</span>}
      </span>
      {subtitle && <span className="stat-change">{subtitle}</span>}
    </div>
  );
}
