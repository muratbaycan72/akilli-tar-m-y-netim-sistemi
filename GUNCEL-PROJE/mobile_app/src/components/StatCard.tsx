import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { colors, radius, spacing } from '../utils/theme';

interface StatCardProps {
  label: string;
  value: string;
  unit?: string;
  accent?: string;
  style?: ViewStyle;
}

export default function StatCard({ label, value, unit, accent = colors.primary, style }: StatCardProps) {
  return (
    <View style={[styles.card, { borderLeftColor: accent }, style]}>
      <Text style={styles.label}>{label}</Text>
      <Text style={styles.value}>
        {value}
        {unit ? <Text style={styles.unit}> {unit}</Text> : null}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    padding: spacing.md,
    borderLeftWidth: 4,
    flex: 1,
    minWidth: '45%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  label: { fontSize: 12, color: colors.textMuted, fontWeight: '500', marginBottom: 4 },
  value: { fontSize: 24, fontWeight: '700', color: colors.text },
  unit: { fontSize: 14, fontWeight: '400', color: colors.textMuted },
});
