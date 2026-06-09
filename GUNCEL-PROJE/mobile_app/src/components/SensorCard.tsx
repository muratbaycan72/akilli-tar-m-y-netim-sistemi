import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { SENSOR_COLORS, SENSOR_LABELS, colors, radius, spacing } from '../utils/theme';
import type { SensorReading } from '../types';
import { formatTime } from '../hooks/useFieldData';

interface SensorCardProps {
  reading: SensorReading;
  onPress?: () => void;
}

export default function SensorCard({ reading, onPress }: SensorCardProps) {
  const type = reading.sensor_type || 'unknown';
  const accent = SENSOR_COLORS[type] || colors.primary;

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={onPress ? 0.7 : 1}>
      <View style={[styles.dot, { backgroundColor: accent }]} />
      <View style={styles.content}>
        <Text style={styles.label}>{SENSOR_LABELS[type] || type}</Text>
        <Text style={styles.value}>
          {reading.value.toFixed(1)} <Text style={styles.unit}>{reading.unit}</Text>
        </Text>
        <Text style={styles.time}>{formatTime(reading.recorded_at)}</Text>
      </View>
      {onPress && <Text style={styles.chevron}>›</Text>}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    padding: spacing.md,
    marginBottom: spacing.sm,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  dot: { width: 10, height: 10, borderRadius: 5, marginRight: spacing.md },
  content: { flex: 1 },
  label: { fontSize: 13, color: colors.textMuted, fontWeight: '500' },
  value: { fontSize: 22, fontWeight: '700', color: colors.text, marginTop: 2 },
  unit: { fontSize: 14, fontWeight: '400', color: colors.textMuted },
  time: { fontSize: 11, color: colors.textMuted, marginTop: 4 },
  chevron: { fontSize: 24, color: colors.textMuted },
});
