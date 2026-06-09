import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors, radius, spacing } from '../utils/theme';
import type { Alert } from '../types';

interface AlertItemProps {
  alert: Alert;
}

export default function AlertItem({ alert }: AlertItemProps) {
  const borderColor =
    alert.severity === 'critical'
      ? colors.danger
      : alert.severity === 'warning'
        ? colors.warning
        : colors.info;

  return (
    <View style={[styles.card, { borderLeftColor: borderColor }]}>
      <Text style={styles.title}>{alert.title}</Text>
      <Text style={styles.message}>{alert.message}</Text>
      <Text style={styles.time}>
        {new Date(alert.created_at).toLocaleString('tr-TR')}
        {!alert.is_read ? ' · Okunmadı' : ''}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    padding: spacing.md,
    marginBottom: spacing.sm,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  title: { fontSize: 15, fontWeight: '600', color: colors.text },
  message: { fontSize: 13, color: colors.textMuted, marginTop: 4 },
  time: { fontSize: 11, color: colors.textMuted, marginTop: 8 },
});
