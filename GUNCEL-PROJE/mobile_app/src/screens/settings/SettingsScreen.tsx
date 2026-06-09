import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { useApp } from '../../context/AppContext';
import { BASE_URL } from '../../services/api';
import { colors, spacing, radius } from '../../utils/theme';

export default function SettingsScreen() {
  const { fields, selectedField, setSelectedField, loading, refreshFields } = useApp();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Ayarlar</Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Tarla Seçimi</Text>
        {loading ? (
          <ActivityIndicator color={colors.primary} />
        ) : (
          fields.map((field) => (
            <TouchableOpacity
              key={field.id}
              style={[
                styles.fieldOption,
                selectedField?.id === field.id && styles.fieldSelected,
              ]}
              onPress={() => setSelectedField(field)}
            >
              <Text style={styles.fieldName}>{field.name}</Text>
              <Text style={styles.fieldMeta}>
                {field.crop_type || '—'} · {field.location || 'Konum yok'}
              </Text>
              {selectedField?.id === field.id && (
                <Text style={styles.check}>✓ Seçili</Text>
              )}
            </TouchableOpacity>
          ))
        )}
        <TouchableOpacity style={styles.refreshBtn} onPress={refreshFields}>
          <Text style={styles.refreshText}>Yenile</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Bağlantı</Text>
        <Text style={styles.label}>API Adresi</Text>
        <Text style={styles.apiUrl}>{BASE_URL}</Text>
        <Text style={styles.hint}>
          Android emülatör: 10.0.2.2{'\n'}
          iOS simülatör: localhost{'\n'}
          Fiziksel cihaz: bilgisayar IP adresi
        </Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Uygulama</Text>
        <Text style={styles.version}>Akıllı Tarım v1.0.0</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  title: { fontSize: 22, fontWeight: '700', color: colors.text, marginBottom: spacing.lg },
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    padding: spacing.lg,
    marginBottom: spacing.md,
  },
  cardTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginBottom: spacing.md },
  fieldOption: {
    padding: spacing.md,
    borderRadius: radius.sm,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.sm,
  },
  fieldSelected: { borderColor: colors.primary, backgroundColor: '#f0faf4' },
  fieldName: { fontSize: 15, fontWeight: '600', color: colors.text },
  fieldMeta: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  check: { fontSize: 12, color: colors.primary, fontWeight: '600', marginTop: 4 },
  refreshBtn: { alignItems: 'center', padding: spacing.sm },
  refreshText: { color: colors.primary, fontWeight: '600' },
  label: { fontSize: 12, color: colors.textMuted, fontWeight: '600' },
  apiUrl: { fontSize: 13, color: colors.text, marginTop: 4, fontFamily: 'monospace' },
  hint: { fontSize: 12, color: colors.textMuted, marginTop: spacing.sm, lineHeight: 18 },
  version: { fontSize: 14, color: colors.textMuted },
});
