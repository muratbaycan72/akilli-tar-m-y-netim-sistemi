import { createFileRoute } from "@tanstack/react-router";
import { Thermometer, Droplets, Sun, Wind, Gauge, Leaf } from "lucide-react";

export const Route = createFileRoute("/sensors")({
  component: SensorsPage,
  head: () => ({ meta: [{ title: "Sensör Verileri · AgriMind" }] }),
});

const sensors = [
  { name: "Toprak Nemi #1", value: "34%", status: "warn", icon: Droplets },
  { name: "Toprak Nemi #2", value: "41%", status: "ok", icon: Droplets },
  { name: "Hava Sıcaklığı", value: "28.5°C", status: "ok", icon: Thermometer },
  { name: "Hava Nemi", value: "56%", status: "ok", icon: Droplets },
  { name: "Işık Şiddeti", value: "78%", status: "ok", icon: Sun },
  { name: "Rüzgar Hızı", value: "12 km/s", status: "ok", icon: Wind },
  { name: "Toprak pH", value: "6.7", status: "ok", icon: Gauge },
  { name: "Yaprak Sıcaklığı", value: "26.1°C", status: "ok", icon: Leaf },
];

function SensorsPage() {
  return (
    <div className="px-6 lg:px-10 py-8 max-w-[1600px] mx-auto">
      <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Canlı Veri</div>
      <h1 className="mt-1 text-3xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
        Sensör Verileri
      </h1>
      <p className="text-sm text-muted-foreground mt-1">Tüm sahadaki sensörlerin gerçek zamanlı okumaları.</p>

      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {sensors.map((s) => (
          <div key={s.name} className="rounded-2xl border border-border bg-card p-5">
            <div className="flex items-center justify-between">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-background/40 text-primary">
                <s.icon className="h-5 w-5" />
              </div>
              <span className={`text-[10px] uppercase tracking-widest ${s.status === "warn" ? "text-amber-400" : "text-primary"}`}>
                {s.status === "warn" ? "uyarı" : "normal"}
              </span>
            </div>
            <div className="mt-4 text-xs text-muted-foreground">{s.name}</div>
            <div className="text-2xl font-semibold mt-1" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>{s.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}