import { createServerFn } from "@tanstack/react-start";
import { createClient } from "@supabase/supabase-js";

const supabaseAdmin = createClient(
  process.env.SUPABASE_URL || "",
  process.env.SUPABASE_KEY || ""
);

export type SensorReading = { t: string; temp: number; hum: number };

export type LatestSensorPayload = {
  latest: { temp: number; hum: number; status: string; updatedAt: string } | null;
  series: SensorReading[];
  source: "db" | "empty" | "error";
};

export const getLatestSensorData = createServerFn({ method: "GET" }).handler(async (): Promise<LatestSensorPayload> => {
  try {
    const { data: rows, error } = await supabaseAdmin
      .from("sensor_olcumleri")
      .select("zaman, sicaklik, nem")
      .order("zaman", { ascending: false })
      .limit(30);

    if (error || !rows) return { latest: null, series: [], source: "empty" };

    const series = [...rows].reverse().map((r) => ({
      t: new Date(r.zaman).toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" }),
      temp: Number(r.sicaklik),
      hum: Number(r.nem),
    }));

    return {
      latest: { temp: Number(rows[0].sicaklik), hum: Number(rows[0].nem), status: "Aktif", updatedAt: new Date(rows[0].zaman).toISOString() },
      series,
      source: "db",
    };
  } catch {
    return { latest: null, series: [], source: "error" };
  }
});