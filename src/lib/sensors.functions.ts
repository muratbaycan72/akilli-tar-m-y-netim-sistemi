import { createServerFn } from "@tanstack/react-start";
import { createClient } from "@supabase/supabase-js";

// Şifreleri sildik, GitHub hata vermesin diye boş bıraktık
const supabaseUrl = process.env.SUPABASE_URL || "";
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || "";

const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey);

export type SensorReading = {
  t: string;
  temp: number;
  hum: number;
};

export type LatestSensorPayload = {
  latest: { temp: number; hum: number; status: string; updatedAt: string } | null;
  series: SensorReading[];
  source: "db" | "empty" | "error";
  error?: string;
};

export const getLatestSensorData = createServerFn({ method: "GET" }).handler(
  async (): Promise<LatestSensorPayload> => {
    try {
      const { data: rows, error } = await supabaseAdmin
        .from("sensor_olcumleri")
        .select("zaman, sicaklik, nem")
        .order("zaman", { ascending: false })
        .limit(30);

      if (error) throw error;
      if (!rows || rows.length === 0) {
        return { latest: null, series: [], source: "empty" };
      }

      const ordered = [...rows].reverse();
      const series: SensorReading[] = ordered.map((r) => ({
        t: new Date(r.zaman).toLocaleTimeString("tr-TR", {
          hour: "2-digit",
          minute: "2-digit",
        }),
        temp: Number(r.sicaklik),
        hum: Number(r.nem),
      }));

      const last = rows[0];
      return {
        latest: {
          temp: Number(last.sicaklik),
          hum: Number(last.nem),
          status: "Aktif",
          updatedAt: new Date(last.zaman).toISOString(),
        },
        series,
        source: "db",
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : "Bilinmeyen hata";
      console.error("getLatestSensorData failed:", message);
      return { latest: null, series: [], source: "error", error: message };
    }
  }
);