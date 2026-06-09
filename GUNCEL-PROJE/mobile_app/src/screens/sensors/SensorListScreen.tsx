import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useApp } from '../../context/AppContext';
import { useFieldData } from '../../hooks/useFieldData';
import SensorCard from '../../components/SensorCard';
import { colors, spacing } from '../../utils/theme';
import type { SensorsStackParamList } from '../../navigation/types';

export default function SensorListScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<SensorsStackParamList>>();
  const { selectedField } = useApp();
  const { latest, loading, error, refresh } = useFieldData(selectedField?.id ?? null);

  if (!selectedField) {
    return (
      <View style={styles.center}>
        <Text style={styles.emptyText}>Tarla seçilmedi</Text>
      </View>
    );
  }

  if (loading && latest.length === 0) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={loading} onRefresh={refresh} tintColor={colors.primary} />}
    >
      {error && (
        <View style={styles.errorBanner}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      <Text style={styles.title}>Sensör Durumu</Text>
      <Text style={styles.subtitle}>{selectedField.name} · Gerçek zamanlı</Text>

      {latest.length === 0 ? (
        <Text style={styles.emptyText}>Veri bekleniyor. IoT simülatörlerini çalıştırın.</Text>
      ) : (
        latest.map((r) => (
          <SensorCard
            key={r.id}
            reading={r}
            onPress={() =>
              navigation.navigate('SensorDetail', {
                sensorType: r.sensor_type || 'unknown',
                unit: r.unit,
              })
            }
          />
        ))
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: '700', color: colors.text },
  subtitle: { fontSize: 14, color: colors.textMuted, marginBottom: spacing.lg },
  emptyText: { fontSize: 14, color: colors.textMuted, textAlign: 'center', marginTop: spacing.xl },
  errorBanner: { backgroundColor: '#fde8e8', padding: spacing.md, borderRadius: 8, marginBottom: spacing.md },
  errorText: { color: colors.danger, fontSize: 13 },
});
