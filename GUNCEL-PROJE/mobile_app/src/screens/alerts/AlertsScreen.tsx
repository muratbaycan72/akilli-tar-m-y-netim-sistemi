import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
} from 'react-native';
import { useApp } from '../../context/AppContext';
import { useAlerts } from '../../hooks/useFieldData';
import AlertItem from '../../components/AlertItem';
import { colors, spacing } from '../../utils/theme';

export default function AlertsScreen() {
  const { selectedField } = useApp();
  const { alerts, refresh } = useAlerts(selectedField?.user_id ?? null);
  const [refreshing, setRefreshing] = React.useState(false);

  const filtered = selectedField
    ? alerts.filter((a) => a.field_id === selectedField.id)
    : alerts;

  const onRefresh = async () => {
    setRefreshing(true);
    await refresh();
    setRefreshing(false);
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />
      }
    >
      <Text style={styles.title}>Bildirimler</Text>
      <Text style={styles.subtitle}>
        {filtered.filter((a) => !a.is_read).length} okunmamış
      </Text>

      {filtered.length === 0 ? (
        <View style={styles.empty}>
          <Text style={styles.emptyIcon}>✅</Text>
          <Text style={styles.emptyTitle}>Alarm yok</Text>
          <Text style={styles.emptyText}>Tüm sistemler normal çalışıyor.</Text>
        </View>
      ) : (
        filtered.map((alert) => <AlertItem key={alert.id} alert={alert} />)
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  title: { fontSize: 22, fontWeight: '700', color: colors.text },
  subtitle: { fontSize: 14, color: colors.textMuted, marginBottom: spacing.lg },
  empty: { alignItems: 'center', paddingTop: spacing.xl * 2 },
  emptyIcon: { fontSize: 48 },
  emptyTitle: { fontSize: 18, fontWeight: '600', color: colors.text, marginTop: spacing.md },
  emptyText: { fontSize: 14, color: colors.textMuted, marginTop: spacing.sm },
});
