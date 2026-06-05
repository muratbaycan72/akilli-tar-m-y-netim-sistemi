import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useServerFn } from "@tanstack/react-start";
import { getLatestSensorData } from "@/lib/sensors.functions";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  Thermometer,
  Droplets,
  Activity,
  AlertTriangle,
  Brain,
  Power,
  Wifi,
  Sun,
  Wind,
} from "lucide-react";

type Point = { t: string; temp: number; hum: number };

function seed(): Point[] {
  const out: Point[] = [];
  const now = Date.now();
  for (let i = 29; i >= 0; i--) {
    const d = new Date(now - i * 60_000);
    out.push({
      t: d.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" }),
      temp: +(27 + Math.sin(i / 3) * 1.5 + Math.random()).toFixed(1),
      hum: +(36 + Math.cos(i / 4) * 4 + Math.random() * 2).toFixed(1),
    });
  }
  return out;
}

export function Dashboard() {
  const [data, setData] = useState<Point[]>(() => seed());
  const [temp, setTemp] = useState(28.5);
  const [hum, setHum] = useState(34);
  const [valveOn, setValveOn] = useState(false);
  const [pulse, setPulse] = useState(false);

  const fetchLatest = useServerFn(getLatestSensorData);
  const { data: live } = useQuery({
    queryKey: ["sensor-latest"],
    queryFn: () => fetchLatest(),
    refetchInterval: 5_000,
    refetchOnWindowFocus: false,
  });

  const dbConnected = live?.source === "db";
  const dbError = live?.source === "error" ? live.error : null;

  useEffect(() => {
    if (live?.source === "db" && live.series.length > 0 && live.latest) {
      setData(live.series);
      setTemp(live.latest.temp);
      setHum(live.latest.hum);
    }
  }, [live]);

  useEffect(() => {
    if (live?.source === "db") return; // canlı veri var, simülasyonu durdur
    const id = setInterval(() => {
      setData((prev) => {
        const last = prev[prev.length - 1];
        const newTemp = +(last.temp + (Math.random() - 0.5) * 0.6).toFixed(1);
        const newHum = valveOn
          ? +(Math.min(80, last.hum + Math.random() * 2)).toFixed(1)
          : +(Math.max(15, last.hum - Math.random() * 0.6)).toFixed(1);
        setTemp(newTemp);
        setHum(newHum);
        const next = [
          ...prev.slice(1),
          {
            t: new Date().toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
            temp: newTemp,
            hum: newHum,
          },
        ];
        return next;
      });
    }, 1500);
    return () => clearInterval(id);
  }, [valveOn, live?.source]);

  const critical = hum < 35;

  const toggleValve = () => {
    setValveOn((v) => !v);
    setPulse(true);
    setTimeout(() => setPulse(false), 800);
  };

  return (
    <div className="px-6 lg:px-10 py-8 space-y-8 max-w-[1600px] mx-auto">
      <Header dbConnected={dbConnected} dbError={dbError} />

      {/* Summary cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <SummaryCard
          icon={<Thermometer className="h-5 w-5" />}
          label="Canlı Sıcaklık"
          value={`${temp.toFixed(1)}°C`}
          accent="from-orange-500/20 to-rose-500/5"
          iconColor="text-orange-400"
          trend="+0.4°"
        />
        <SummaryCard
          icon={<Droplets className="h-5 w-5" />}
          label="Toprak Nemi"
          value={`%${hum.toFixed(0)}`}
          accent="from-sky-500/20 to-cyan-500/5"
          iconColor="text-sky-400"
          trend={valveOn ? "+yükseliyor" : "-azalıyor"}
        />
        <SummaryCard
          icon={<Activity className="h-5 w-5" />}
          label="Sistem Durumu"
          value="Aktif"
          accent="from-emerald-500/20 to-teal-500/5"
          iconColor="text-primary"
          trend="Tüm sensörler bağlı"
          live
        />
      </div>

      {/* Chart + AI box */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 rounded-2xl border border-border bg-card p-6 shadow-[0_1px_0_0_rgba(255,255,255,0.04)_inset]">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                Canlı Sensör Akışı
              </h2>
              <p className="text-sm text-muted-foreground">Son 30 dakika · sıcaklık & nem</p>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <Legend color="oklch(0.78 0.18 145)" label="Nem (%)" />
              <Legend color="oklch(0.75 0.18 60)" label="Sıcaklık (°C)" />
            </div>
          </div>
          <div className="h-[320px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
                <defs>
                  <linearGradient id="g-hum" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="oklch(0.78 0.18 145)" stopOpacity={0.55} />
                    <stop offset="100%" stopColor="oklch(0.78 0.18 145)" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="g-temp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="oklch(0.75 0.18 60)" stopOpacity={0.45} />
                    <stop offset="100%" stopColor="oklch(0.75 0.18 60)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="oklch(0.3 0.02 160)" vertical={false} />
                <XAxis dataKey="t" stroke="oklch(0.6 0.02 160)" fontSize={11} tickLine={false} axisLine={false} interval={4} />
                <YAxis stroke="oklch(0.6 0.02 160)" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    background: "oklch(0.18 0.02 160)",
                    border: "1px solid oklch(0.3 0.02 160)",
                    borderRadius: 8,
                    fontSize: 12,
                  }}
                />
                <Area type="monotone" dataKey="hum" stroke="oklch(0.78 0.18 145)" strokeWidth={2} fill="url(#g-hum)" isAnimationActive />
                <Area type="monotone" dataKey="temp" stroke="oklch(0.75 0.18 60)" strokeWidth={2} fill="url(#g-temp)" isAnimationActive />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <AiPredictionBox critical={critical} hum={hum} />
      </div>

      {/* Valve */}
      <ValveControl on={valveOn} pulse={pulse} onToggle={toggleValve} />

      {/* Mini stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MiniStat icon={<Sun className="h-4 w-4" />} label="Işık" value="78%" />
        <MiniStat icon={<Wind className="h-4 w-4" />} label="Rüzgar" value="12 km/s" />
        <MiniStat icon={<Droplets className="h-4 w-4" />} label="Hava Nemi" value="56%" />
        <MiniStat icon={<Wifi className="h-4 w-4" />} label="Bağlantı" value="Güçlü" />
      </div>
    </div>
  );
}

function Header({ dbConnected, dbError }: { dbConnected: boolean; dbError?: string | null }) {
  const today = new Date().toLocaleDateString("tr-TR", { weekday: "long", day: "numeric", month: "long" });
  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div>
        <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Genel Bakış</div>
        <h1 className="mt-1 text-3xl md:text-4xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
          Tarla A‑12 · Akıllı Panel
        </h1>
        <p className="text-sm text-muted-foreground mt-1 capitalize">{today}</p>
      </div>
      <div className="flex flex-col items-end gap-1">
        <div className="flex items-center gap-2 rounded-full border border-border bg-card px-4 py-2 text-xs">
          <span className="relative flex h-2 w-2">
            <span className={`absolute inline-flex h-full w-full rounded-full opacity-75 animate-ping ${dbConnected ? "bg-primary" : "bg-amber-400"}`}></span>
            <span className={`relative inline-flex h-2 w-2 rounded-full ${dbConnected ? "bg-primary" : "bg-amber-400"}`}></span>
          </span>
          {dbConnected ? "Lovable Cloud · canlı veri" : "Simülasyon modu"}
        </div>
        {dbError && (
          <span className="text-[10px] text-amber-400/80 max-w-xs truncate" title={dbError}>
            DB: {dbError}
          </span>
        )}
      </div>
    </div>
  );
}

function SummaryCard({
  icon, label, value, accent, iconColor, trend, live,
}: { icon: React.ReactNode; label: string; value: string; accent: string; iconColor: string; trend: string; live?: boolean }) {
  return (
    <div className={`relative overflow-hidden rounded-2xl border border-border bg-card p-5`}>
      <div className={`absolute inset-0 bg-gradient-to-br ${accent} pointer-events-none`} />
      <div className="relative">
        <div className="flex items-center justify-between">
          <div className={`flex h-10 w-10 items-center justify-center rounded-xl bg-background/40 ring-1 ring-border ${iconColor}`}>
            {icon}
          </div>
          {live && (
            <span className="flex items-center gap-1.5 text-[10px] uppercase tracking-widest text-primary">
              <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" /> live
            </span>
          )}
        </div>
        <div className="mt-5 text-xs uppercase tracking-widest text-muted-foreground">{label}</div>
        <div className="mt-1 text-3xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>{value}</div>
        <div className="mt-2 text-xs text-muted-foreground">{trend}</div>
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span className="flex items-center gap-1.5 text-muted-foreground">
      <span className="h-2 w-2 rounded-full" style={{ background: color }} />
      {label}
    </span>
  );
}

function AiPredictionBox({ critical, hum }: { critical: boolean; hum: number }) {
  const tone = critical
    ? "from-amber-500/25 via-rose-500/20 to-rose-600/10 border-amber-500/50"
    : "from-emerald-500/15 to-teal-500/5 border-primary/30";
  return (
    <div className={`relative rounded-2xl border bg-gradient-to-br ${tone} p-6 overflow-hidden`}>
      <div className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-amber-400/10 blur-3xl" />
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-amber-300">
        <Brain className="h-4 w-4" /> Yapay Zeka Sulama Tahmini
      </div>

      <div className="mt-5 flex items-start gap-3">
        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${critical ? "bg-amber-500/20 text-amber-300" : "bg-primary/20 text-primary"}`}>
          <AlertTriangle className="h-5 w-5" />
        </div>
        <div>
          <div className="text-lg font-semibold leading-snug" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            {critical
              ? "Toprak nemi kritik sınırda."
              : "Toprak nemi normal aralıkta."}
          </div>
          <p className="mt-2 text-sm text-foreground/80">
            Yapay zeka modeline göre toprak nemi {hum.toFixed(0)}% seviyesinde.
            {critical ? " 2 saat içinde sulama başlatılmalı!" : " Önümüzdeki 6 saat için sulama önerilmiyor."}
          </p>
        </div>
      </div>

      <div className="mt-6 space-y-3">
        <Confidence label="Model Güveni" value={92} />
        <Confidence label="Sulama Aciliyeti" value={critical ? 86 : 22} warn={critical} />
      </div>

      <div className="mt-6 flex items-center justify-between text-xs text-muted-foreground">
        <span>Model: AgriNet v3.2</span>
        <span>Son güncelleme · az önce</span>
      </div>
    </div>
  );
}

function Confidence({ label, value, warn }: { label: string; value: number; warn?: boolean }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-muted-foreground mb-1">
        <span>{label}</span><span>{value}%</span>
      </div>
      <div className="h-1.5 rounded-full bg-background/40 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${warn ? "bg-gradient-to-r from-amber-400 to-rose-500" : "bg-gradient-to-r from-primary to-emerald-300"}`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

function ValveControl({ on, pulse, onToggle }: { on: boolean; pulse: boolean; onToggle: () => void }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-border bg-card p-6 md:p-8">
      <div className="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-6 items-center">
        <div>
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Uzaktan Kontrol</div>
          <h3 className="mt-1 text-2xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            Sanal Sulama Vanası
          </h3>
          <p className="mt-2 text-sm text-muted-foreground max-w-md">
            Vanayı uzaktan açıp kapatın. Su debisi ve süre, sistem tarafından otomatik olarak izlenir.
          </p>
          <div className="mt-4 inline-flex items-center gap-2 rounded-full border border-border bg-background/40 px-3 py-1.5 text-xs">
            <span className={`h-2 w-2 rounded-full ${on ? "bg-sky-400 animate-pulse" : "bg-muted-foreground/50"}`} />
            <span className="font-medium">
              {on ? "Sulama Başlatıldı" : "Sulama Durduruldu"}
            </span>
          </div>
        </div>

        <div className="flex flex-col items-center gap-3">
          <button
            onClick={onToggle}
            className={`relative flex h-28 w-28 items-center justify-center rounded-full transition-all duration-300 active:scale-95 ${
              on
                ? "bg-gradient-to-br from-sky-400 to-cyan-600 text-white shadow-[0_0_40px_-5px_oklch(0.7_0.16_220)]"
                : "bg-gradient-to-br from-secondary to-card text-foreground border border-border"
            }`}
            style={pulse ? { animation: "pulse-glow 0.8s ease-out" } : undefined}
            aria-label="Vana kontrolü"
          >
            <Power className={`h-10 w-10 ${on ? "" : "text-primary"}`} />
            {on && (
              <>
                <span className="absolute inset-0 rounded-full border border-white/30" style={{ animation: "ripple 1.6s ease-out infinite" }} />
                <span className="absolute inset-0 rounded-full border border-white/20" style={{ animation: "ripple 1.6s ease-out 0.6s infinite" }} />
              </>
            )}
            {on && (
              <div className="absolute -bottom-3 left-1/2 -translate-x-1/2 flex gap-1">
                {[0, 1, 2].map((i) => (
                  <span
                    key={i}
                    className="block h-2 w-1 rounded-full bg-sky-400"
                    style={{ animation: `drip 1.1s ease-in ${i * 0.25}s infinite` }}
                  />
                ))}
              </div>
            )}
          </button>
          <span className="text-xs uppercase tracking-widest text-muted-foreground">
            {on ? "Açık" : "Kapalı"} · tıklayın
          </span>
        </div>
      </div>
    </div>
  );
}

function MiniStat({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="rounded-xl border border-border bg-card/60 p-4 flex items-center gap-3">
      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-background/40 text-primary">{icon}</div>
      <div>
        <div className="text-xs text-muted-foreground">{label}</div>
        <div className="text-sm font-semibold">{value}</div>
      </div>
    </div>
  );
}