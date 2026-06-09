import { createFileRoute } from "@tanstack/react-router";
import { Brain, Sparkles, TrendingUp, AlertTriangle } from "lucide-react";

export const Route = createFileRoute("/ai")({
  component: AiPage,
  head: () => ({ meta: [{ title: "Yapay Zeka Tahminleri · AgriMind" }] }),
});

function AiPage() {
  return (
    <div className="px-6 lg:px-10 py-8 max-w-[1600px] mx-auto space-y-6">
      <div>
        <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">AgriNet v3.2</div>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
          Yapay Zeka Tahminleri
        </h1>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {[
          { title: "Sulama Önerisi", desc: "2 saat içinde sulama başlatın.", icon: AlertTriangle, tone: "amber" },
          { title: "Verim Tahmini", desc: "Hasat: 4.8 ton / hektar (±%6).", icon: TrendingUp, tone: "emerald" },
          { title: "Hastalık Riski", desc: "Mantar riski düşük — %12.", icon: Sparkles, tone: "emerald" },
        ].map((c) => (
          <div key={c.title} className="rounded-2xl border border-border bg-card p-6">
            <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${c.tone === "amber" ? "bg-amber-500/15 text-amber-400" : "bg-primary/15 text-primary"}`}>
              <c.icon className="h-5 w-5" />
            </div>
            <div className="mt-4 font-semibold" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>{c.title}</div>
            <p className="text-sm text-muted-foreground mt-1">{c.desc}</p>
          </div>
        ))}
      </div>
      <div className="rounded-2xl border border-border bg-card p-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Brain className="h-4 w-4 text-primary" /> Model son 24 saatte 1.284 veri noktası işledi.
        </div>
      </div>
    </div>
  );
}