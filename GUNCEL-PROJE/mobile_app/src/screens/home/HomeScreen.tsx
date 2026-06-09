import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useApp } from '../../context/AppContext';
import { useFieldData } from '../../hooks/useFieldData';
import StatCard from '../../components/StatCard';
import SensorCard from '../../components/SensorCard';
import { colors, spacing } from '../../utils/theme';
import { checkMoistureAlert, requestNotificationPermission } from '../../services/notifications';

export default function HomeScreen() {
  const { selectedField, loading: fieldsLoading, error: fieldsError } = useApp();
  const { latest, predictions, loading, error, refresh } = useFieldData(
    selectedField?.id ?? null,
  );

  useEffect(() => {
    requestNotificationPermission();
  }, []);

  useEffect(() => {
    const soil = latest.find((r) => r.sensor_type === 'soil_moisture');
    if (soil && selectedField) {
      checkMoistureAlert(soil.value, selectedField.name);
    }
  }, [latest, selectedField]);

  if (fieldsLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (!selectedField) {
    return (
      <View style={styles.center}>
        <Text style={styles.emptyTitle}>Tarla Bulunamadı</Text>
        <Text style={styles.emptyText}>Backend'de seed verisi oluşturun.</Text>
      </View>
    );
  }

  const soil = latest.find((r) => r.sensor_type === 'soil_moisture');
  const temp = latest.find((r) => r.sensor_type === 'temperature');
  const humidity = latest.find((r) => r.sensor_type === 'humidity');
  const lastPred = predictions.find((p) => p.prediction_type === 'soil_moisture');

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={loading} onRefresh={refresh} tintColor={colors.primary} />}
    >
      {(error || fieldsError) && (
        <View style={styles.errorBanner}>
          <Text style={styles.errorText}>{error || fieldsError}</Text>
        </View>
      )}

      <View style={styles.header}>
        <Text style={styles.greeting}>Merhaba 👋</Text>
        <Text style={styles.fieldName}>{selectedField.name}</Text>
        {selectedField.crop_type && (
          <Text style={styles.subtitle}>{selectedField.crop_type} · {selectedField.location || 'Türkiye'}</Text>
        )}
      </View>

      <View style={styles.statRow}>
        <StatCard
          label="Toprak Nemi"
          value={soil ? soil.value.toFixed(1) : '—'}
          unit={soil?.unit ?? '%'}
          accent={soil && soil.value < 30 ? colors.danger : colors.primary}
        />
        <StatCard
          label="Sıcaklık"
          value={temp ? temp.value.toFixed(1) : '—'}
          unit={temp?.unit ?? '°C'}
          accent={colors.info}
        />
      </View>
      <View style={styles.statRow}>
        <StatCard
          label="Hava Nemi"
          value={humidity ? humidity.value.toFixed(1) : '—'}
          unit={humidity?.unit ?? '%'}
        />
        <StatCard
          label="ML Tahmin"
          value={lastPred ? lastPred.predicted_value.toFixed(1) : '—'}
          unit="%"
          accent={colors.warning}
        />
      </View>

      <Text style={styles.sectionTitle}>Anlık Sensörler</Text>
      {latest.length === 0 ? (
        <Text style={styles.emptyText}>Henüz sensör verisi yok.</Text>
      ) : (
        latest.map((r) => <SensorCard key={r.id} reading={r} />)
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg, paddingBottom: spacing.xl },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  header: { marginBottom: spacing.lg },
  greeting: { fontSize: 14, color: colors.textMuted },
  fieldName: { fontSize: 26, fontWeight: '700', color: colors.text, marginTop: 4 },
  subtitle: { fontSize: 14, color: colors.textMuted, marginTop: 4 },
  statRow: { flexDirection: 'row', gap: spacing.sm, marginBottom: spacing.sm },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginTop: spacing.md, marginBottom: spacing.sm },
  emptyTitle: { fontSize: 18, fontWeight: '600', color: colors.text },
  emptyText: { fontSize: 14, color: colors.textMuted, marginTop: 8, textAlign: 'center' },
  errorBanner: { backgroundColor: '#fde8e8', padding: spacing.md, borderRadius: 8, marginBottom: spacing.md },
  errorText: { color: colors.danger, fontSize: 13 },
});
