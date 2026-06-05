import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/settings")({
  component: SettingsPage,
  head: () => ({ meta: [{ title: "Ayarlar · AgriMind" }] }),
});

function SettingsPage() {
  return (
    <div className="px-6 lg:px-10 py-8 max-w-[1600px] mx-auto space-y-6">
      <div>
        <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Sistem</div>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
          Ayarlar
        </h1>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {[
          { k: "Otomatik Sulama Eşiği", v: "30% nem" },
          { k: "Bildirimler", v: "E‑posta + Mobil" },
          { k: "Veri Aralığı", v: "Her 1.5 saniye" },
          { k: "Bölge", v: "Tarla A‑12" },
        ].map((it) => (
          <div key={it.k} className="rounded-2xl border border-border bg-card p-5 flex items-center justify-between">
            <div>
              <div className="text-xs text-muted-foreground uppercase tracking-widest">{it.k}</div>
              <div className="font-semibold mt-1">{it.v}</div>
            </div>
            <button className="text-xs rounded-md border border-border px-3 py-1.5 hover:bg-secondary transition">Düzenle</button>
          </div>
        ))}
      </div>
    </div>
  );
}