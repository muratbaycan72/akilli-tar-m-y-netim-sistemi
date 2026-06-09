export const MQTT_TOPIC_PREFIX = 'akilli-tarim';

export const SENSOR_TYPES = [
  'soil_moisture',
  'temperature',
  'humidity',
  'light',
  'ph',
  'plant_health',
] as const;

export type SensorType = (typeof SENSOR_TYPES)[number];

export const buildSensorTopic = (fieldId: string, sensorType: SensorType): string =>
  `${MQTT_TOPIC_PREFIX}/${fieldId}/sensors/${sensorType}`;

export const buildCommandTopic = (fieldId: string, action: string): string =>
  `${MQTT_TOPIC_PREFIX}/${fieldId}/commands/${action}`;
