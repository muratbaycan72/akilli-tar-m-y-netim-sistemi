import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { colors, radius, spacing, SENSOR_LABELS } from '../utils/theme';
import type { SensorReading } from '../types';

interface MiniChartProps {
  readings: SensorReading[];
  sensorType: string;
  color?: string;
}

const screenWidth = Dimensions.get('window').width - spacing.lg * 2;

export default function MiniChart({ readings, sensorType, color = colors.primary }: MiniChartProps) {
  if (readings.length < 2) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>Grafik için yeterli veri yok</Text>
      </View>
    );
  }

  const data = readings.slice(-10);
  const labels = data.map((_, i) => (i % 2 === 0 ? `${i + 1}` : ''));

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{SENSOR_LABELS[sensorType] || sensorType}</Text>
      <LineChart
        data={{
          labels,
          datasets: [{ data: data.map((r) => r.value), color: () => color, strokeWidth: 2 }],
        }}
        width={screenWidth - spacing.md * 2}
        height={180}
        chartConfig={{
          backgroundColor: colors.surface,
          backgroundGradientFrom: colors.surface,
          backgroundGradientTo: colors.surface,
          decimalPlaces: 1,
          color: () => color,
          labelColor: () => colors.textMuted,
          propsForDots: { r: '4', strokeWidth: '2', stroke: color },
          propsForBackgroundLines: { stroke: colors.border },
        }}
        bezier
        style={styles.chart}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  title: { fontSize: 15, fontWeight: '600', color: colors.text, marginBottom: spacing.sm },
  chart: { borderRadius: radius.sm },
  empty: { padding: spacing.lg, alignItems: 'center' },
  emptyText: { color: colors.textMuted, fontSize: 13 },
});
