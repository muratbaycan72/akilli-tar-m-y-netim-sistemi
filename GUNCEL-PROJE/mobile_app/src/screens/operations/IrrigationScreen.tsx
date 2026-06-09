import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  RefreshControl,
} from 'react-native';
import { useApp } from '../../context/AppContext';
import { useFieldData, formatTime } from '../../hooks/useFieldData';
import ControlButton from '../../components/ControlButton';
import { api } from '../../services/api';
import { sendLocalAlert } from '../../services/notifications';
import { colors, spacing, radius } from '../../utils/theme';

export default function IrrigationScreen() {
  const { selectedField } = useApp();
  const { irrigationLogs, loading, refresh } = useFieldData(selectedField?.id ?? null);
  const [duration, setDuration] = useState('30');
  const [water, setWater] = useState('500');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: 'ok' | 'err'; text: string } | null>(null);

  const handleStart = async () => {
    if (!selectedField) return;
    setSubmitting(true);
    setMessage(null);
    try {
      await api.startIrrigation({
        field_id: selectedField.id,
        duration_minutes: parseInt(duration, 10) || 30,
        water_amount_liters: parseInt(water, 10) || 500,
        notes: 'Mobil uygulama üzerinden tetiklendi',
      });
      setMessage({ type: 'ok', text: `Sulama başlatıldı (${duration} dk)` });
      await sendLocalAlert('Sulama Başlatıldı', `${selectedField.name}: ${duration} dk sulama`, 'info');
      refresh();
    } catch (e) {
      setMessage({ type: 'err', text: e instanceof Error ? e.message : 'Hata oluştu' });
    } finally {
      setSubmitting(false);
    }
  };

  if (!selectedField) {
    return (
      <View style={styles.center}>
        <Text style={styles.empty}>Tarla seçilmedi</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={loading} onRefresh={refresh} tintColor={colors.primary} />}
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>💧 Sulama Kontrolü</Text>
        <Text style={styles.cardSub}>{selectedField.name}</Text>

        {message && (
          <View style={[styles.banner, message.type === 'ok' ? styles.bannerOk : styles.bannerErr]}>
            <Text style={message.type === 'ok' ? styles.bannerOkText : styles.bannerErrText}>
              {message.text}
            </Text>
          </View>
        )}

        <Text style={styles.label}>Süre (dakika)</Text>
        <TextInput
          style={styles.input}
          value={duration}
          onChangeText={setDuration}
          keyboardType="number-pad"
        />

        <Text style={styles.label}>Su Miktarı (litre)</Text>
        <TextInput
          style={styles.input}
          value={water}
          onChangeText={setWater}
          keyboardType="number-pad"
        />

        <ControlButton
          title="🚿 Sulamayı Başlat"
          onPress={handleStart}
          loading={submitting}
        />
      </View>

      <Text style={styles.sectionTitle}>Sulama Geçmişi</Text>
      {irrigationLogs.length === 0 ? (
        <Text style={styles.empty}>Henüz kayıt yok</Text>
      ) : (
        irrigationLogs.map((log) => (
          <View key={log.id} style={styles.logRow}>
            <View>
              <Text style={styles.logDate}>{formatTime(log.started_at)}</Text>
              <Text style={styles.logDetail}>
                {log.duration_minutes} dk · {log.water_amount_liters ?? '—'} L
              </Text>
            </View>
            <View style={[styles.badge, log.status === 'completed' && styles.badgeOk]}>
              <Text style={styles.badgeText}>{log.status}</Text>
            </View>
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
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  cardTitle: { fontSize: 18, fontWeight: '700', color: colors.text },
  cardSub: { fontSize: 14, color: colors.textMuted, marginBottom: spacing.md },
  label: { fontSize: 13, fontWeight: '600', color: colors.textMuted, marginTop: spacing.sm },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.sm,
    padding: spacing.md,
    fontSize: 16,
    marginTop: spacing.xs,
    backgroundColor: colors.background,
  },
  banner: { padding: spacing.md, borderRadius: radius.sm, marginBottom: spacing.sm },
  bannerOk: { backgroundColor: '#d8f3dc' },
  bannerErr: { backgroundColor: '#fde8e8' },
  bannerOkText: { color: colors.primaryDark, fontSize: 13 },
  bannerErrText: { color: colors.danger, fontSize: 13 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginBottom: spacing.sm },
  logRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: radius.sm,
    marginBottom: spacing.sm,
  },
  logDate: { fontSize: 14, fontWeight: '600', color: colors.text },
  logDetail: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  badge: { backgroundColor: colors.border, paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  badgeOk: { backgroundColor: '#d8f3dc' },
  badgeText: { fontSize: 11, fontWeight: '600', color: colors.text },
  empty: { color: colors.textMuted, fontSize: 14, textAlign: 'center', marginTop: spacing.lg },
});
