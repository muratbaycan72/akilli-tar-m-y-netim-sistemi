import { Link, useRouterState } from "@tanstack/react-router";
import { LayoutDashboard, Activity, Brain, Settings, Leaf } from "lucide-react";

const items = [
  { title: "Dashboard", url: "/", icon: LayoutDashboard },
  { title: "Sensör Verileri", url: "/sensors", icon: Activity },
  { title: "Yapay Zeka Tahminleri", url: "/ai", icon: Brain },
  { title: "Ayarlar", url: "/settings", icon: Settings },
];

export function AppSidebar() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return (
    <aside className="hidden md:flex w-64 shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground">
      <div className="flex items-center gap-2 px-6 py-6 border-b border-sidebar-border">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/15 ring-1 ring-primary/30">
          <Leaf className="h-5 w-5 text-primary" />
        </div>
        <div>
          <div className="font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>AgriMind</div>
          <div className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Smart Farming</div>
        </div>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {items.map((it) => {
          const active = pathname === it.url;
          return (
            <Link
              key={it.url}
              to={it.url}
              className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all ${
                active
                  ? "bg-sidebar-accent text-primary shadow-[inset_2px_0_0_0_var(--primary)]"
                  : "text-sidebar-foreground/70 hover:bg-sidebar-accent/60 hover:text-sidebar-foreground"
              }`}
            >
              <it.icon className={`h-4 w-4 ${active ? "text-primary" : ""}`} />
              <span>{it.title}</span>
            </Link>
          );
        })}
      </nav>
      <div className="px-4 py-4 border-t border-sidebar-border">
        <div className="rounded-lg bg-sidebar-accent/50 p-3 text-xs">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full rounded-full bg-primary opacity-75 animate-ping"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-primary"></span>
            </span>
            <span className="text-sidebar-foreground/80">Sistem Çevrimiçi</span>
          </div>
          <div className="mt-1 text-muted-foreground">5 sensör bağlı</div>
        </div>
      </div>
    </aside>
  );
}