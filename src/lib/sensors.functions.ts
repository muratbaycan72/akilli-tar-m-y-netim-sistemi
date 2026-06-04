import { createServerFn } from "@tanstack/react-start";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://oimtnvybgdseeqgzprxh.supabase.co";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pbXRudnliZ2RzZWVxZ3pwcnhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA1ODcyMjcsImV4cCI6MjA5NjE2MzIyN30.0JzPzA--jgZbHCXAqOdgRFHOEerSD2XNiqNnAvfrjis";

const supabaseAdmin = createClient(supabaseUrl, supabaseKey);

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
      console.error("Supabase bağlantı hatası:", error);
      return { latest: null, series: [], source: "error" };
    }
  }
);