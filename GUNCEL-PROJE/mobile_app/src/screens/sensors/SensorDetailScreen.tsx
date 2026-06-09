import React from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { useRoute, type RouteProp } from '@react-navigation/native';
import { useApp } from '../../context/AppContext';
import { useFieldData, groupBySensorType } from '../../hooks/useFieldData';
import MiniChart from '../../components/MiniChart';
import { colors, spacing, SENSOR_COLORS, SENSOR_LABELS } from '../../utils/theme';
import type { SensorsStackParamList } from '../../navigation/types';

export default function SensorDetailScreen() {
  const route = useRoute<RouteProp<SensorsStackParamList, 'SensorDetail'>>();
  const { sensorType, unit } = route.params;
  const { selectedField } = useApp();
  const { readings, loading } = useFieldData(selectedField?.id ?? null);

  const grouped = groupBySensorType(readings);
  const sensorReadings = grouped[sensorType] || [];
  const latest = sensorReadings[sensorReadings.length - 1];

  if (loading && sensorReadings.length === 0) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{SENSOR_LABELS[sensorType] || sensorType}</Text>

      {latest && (
        <View style={styles.hero}>
          <Text style={styles.heroValue}>
            {latest.value.toFixed(1)}
            <Text style={styles.heroUnit}> {unit}</Text>
          </Text>
          <Text style={styles.heroLabel}>Son okuma</Text>
        </View>
      )}

      <MiniChart
        readings={sensorReadings}
        sensorType={sensorType}
        color={SENSOR_COLORS[sensorType]}
      />

      <Text style={styles.sectionTitle}>Geçmiş Okumalar</Text>
      {sensorReadings.length === 0 ? (
        <Text style={styles.empty}>Veri yok</Text>
      ) : (
        [...sensorReadings].reverse().slice(0, 15).map((r) => (
          <View key={r.id} style={styles.row}>
            <Text style={styles.rowValue}>{r.value.toFixed(1)} {r.unit}</Text>
            <Text style={styles.rowTime}>
              {new Date(r.recorded_at).toLocaleString('tr-TR')}
            </Text>
          </View>
        ))
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: '700', color: colors.text, marginBottom: spacing.md },
  hero: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: spacing.lg,
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  heroValue: { fontSize: 42, fontWeight: '700', color: colors.primary },
  heroUnit: { fontSize: 18, color: colors.textMuted },
  heroLabel: { fontSize: 13, color: colors.textMuted, marginTop: 4 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginBottom: spacing.sm },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  rowValue: { fontSize: 15, fontWeight: '600', color: colors.text },
  rowTime: { fontSize: 12, color: colors.textMuted },
  empty: { color: colors.textMuted, fontSize: 14 },
});
