-- Akilli Tarim Yonetim Sistemi - PostgreSQL Sema
-- Bu dosya Docker ilk baslatmada otomatik calistirilir.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email       VARCHAR(255) NOT NULL UNIQUE,
    full_name   VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    role        VARCHAR(50) NOT NULL DEFAULT 'farmer'
                CHECK (role IN ('admin', 'farmer', 'operator')),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_role ON users (role);

CREATE TABLE fields (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name        VARCHAR(255) NOT NULL,
    location    VARCHAR(500),
    area_hectares FLOAT,
    crop_type   VARCHAR(100),
    latitude    FLOAT,
    longitude   FLOAT,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_fields_user_id ON fields (user_id);
CREATE INDEX idx_fields_crop_type ON fields (crop_type);

CREATE TABLE sensors (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id    UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    sensor_type VARCHAR(50) NOT NULL
                CHECK (sensor_type IN ('soil_moisture', 'temperature', 'humidity', 'light', 'ph', 'plant_health')),
    device_id   VARCHAR(100) NOT NULL UNIQUE,
    unit        VARCHAR(20) NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    installed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sensors_field_id ON sensors (field_id);
CREATE INDEX idx_sensors_type ON sensors (sensor_type);
CREATE INDEX idx_sensors_device_id ON sensors (device_id);

CREATE TABLE sensor_readings (
    id          BIGSERIAL PRIMARY KEY,
    sensor_id   UUID NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    field_id    UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    value       FLOAT NOT NULL,
    unit        VARCHAR(20) NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata    JSONB DEFAULT '{}'
);

CREATE INDEX idx_sensor_readings_sensor_id ON sensor_readings (sensor_id);
CREATE INDEX idx_sensor_readings_field_id ON sensor_readings (field_id);
CREATE INDEX idx_sensor_readings_recorded_at ON sensor_readings (recorded_at DESC);
CREATE INDEX idx_sensor_readings_sensor_time ON sensor_readings (sensor_id, recorded_at DESC);

CREATE TABLE weather_readings (
    id              BIGSERIAL PRIMARY KEY,
    field_id        UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    temperature     FLOAT,
    humidity        FLOAT,
    wind_speed      FLOAT,
    rainfall_mm     FLOAT,
    solar_radiation FLOAT,
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_weather_readings_field_id ON weather_readings (field_id);
CREATE INDEX idx_weather_readings_recorded_at ON weather_readings (recorded_at DESC);

CREATE TABLE plant_health_records (
    id              BIGSERIAL PRIMARY KEY,
    field_id        UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    health_score    FLOAT NOT NULL CHECK (health_score >= 0 AND health_score <= 100),
    disease_detected BOOLEAN NOT NULL DEFAULT FALSE,
    disease_type    VARCHAR(100),
    notes           TEXT,
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_plant_health_field_id ON plant_health_records (field_id);
CREATE INDEX idx_plant_health_recorded_at ON plant_health_records (recorded_at DESC);

CREATE TABLE irrigation_logs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id        UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    triggered_by    VARCHAR(50) NOT NULL DEFAULT 'manual'
                    CHECK (triggered_by IN ('manual', 'automatic', 'scheduled')),
    duration_minutes INTEGER NOT NULL,
    water_amount_liters FLOAT,
    status          VARCHAR(50) NOT NULL DEFAULT 'completed'
                    CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMPTZ,
    notes           TEXT
);

CREATE INDEX idx_irrigation_logs_field_id ON irrigation_logs (field_id);
CREATE INDEX idx_irrigation_logs_started_at ON irrigation_logs (started_at DESC);

CREATE TABLE fertilization_logs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id        UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    fertilizer_type VARCHAR(100) NOT NULL,
    amount_kg       FLOAT NOT NULL,
    triggered_by    VARCHAR(50) NOT NULL DEFAULT 'manual'
                    CHECK (triggered_by IN ('manual', 'automatic', 'scheduled')),
    status          VARCHAR(50) NOT NULL DEFAULT 'completed'
                    CHECK (status IN ('pending', 'completed', 'cancelled')),
    applied_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes           TEXT
);

CREATE INDEX idx_fertilization_logs_field_id ON fertilization_logs (field_id);
CREATE INDEX idx_fertilization_logs_applied_at ON fertilization_logs (applied_at DESC);

CREATE TABLE spraying_logs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id        UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    pesticide_type  VARCHAR(100) NOT NULL,
    amount_liters   FLOAT NOT NULL,
    triggered_by    VARCHAR(50) NOT NULL DEFAULT 'manual'
                    CHECK (triggered_by IN ('manual', 'automatic', 'scheduled')),
    status          VARCHAR(50) NOT NULL DEFAULT 'completed'
                    CHECK (status IN ('pending', 'completed', 'cancelled')),
    applied_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes           TEXT
);

CREATE INDEX idx_spraying_logs_field_id ON spraying_logs (field_id);
CREATE INDEX idx_spraying_logs_applied_at ON spraying_logs (applied_at DESC);

CREATE TABLE ml_predictions (
    id              BIGSERIAL PRIMARY KEY,
    field_id        UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    model_name      VARCHAR(100) NOT NULL,
    model_version   VARCHAR(50) NOT NULL,
    prediction_type VARCHAR(50) NOT NULL
                    CHECK (prediction_type IN ('soil_moisture', 'plant_health', 'irrigation_need', 'anomaly')),
    predicted_value FLOAT NOT NULL,
    confidence      FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    input_features  JSONB DEFAULT '{}',
    predicted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ml_predictions_field_id ON ml_predictions (field_id);
CREATE INDEX idx_ml_predictions_type ON ml_predictions (prediction_type);
CREATE INDEX idx_ml_predictions_predicted_at ON ml_predictions (predicted_at DESC);

CREATE TABLE alerts (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id    UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_type  VARCHAR(50) NOT NULL
                CHECK (alert_type IN ('low_moisture', 'high_temperature', 'disease', 'irrigation', 'system')),
    severity    VARCHAR(20) NOT NULL DEFAULT 'warning'
                CHECK (severity IN ('info', 'warning', 'critical')),
    title       VARCHAR(255) NOT NULL,
    message     TEXT NOT NULL,
    is_read     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alerts_user_id ON alerts (user_id);
CREATE INDEX idx_alerts_field_id ON alerts (field_id);
CREATE INDEX idx_alerts_is_read ON alerts (is_read);
CREATE INDEX idx_alerts_created_at ON alerts (created_at DESC);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_fields_updated_at
    BEFORE UPDATE ON fields
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
