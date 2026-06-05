
CREATE TABLE public.sensor_olcumleri (
  id bigserial PRIMARY KEY,
  sicaklik numeric NOT NULL,
  nem numeric NOT NULL,
  zaman timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX sensor_olcumleri_zaman_idx ON public.sensor_olcumleri (zaman DESC);

ALTER TABLE public.sensor_olcumleri ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Sensor readings are publicly readable"
  ON public.sensor_olcumleri FOR SELECT
  USING (true);

INSERT INTO public.sensor_olcumleri (sicaklik, nem, zaman)
SELECT
  27 + sin(i::float / 3) * 1.5 + random(),
  36 + cos(i::float / 4) * 4 + random() * 2,
  now() - (i || ' minutes')::interval
FROM generate_series(29, 0, -1) AS i;
