import * as Notifications from 'expo-notifications';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export async function requestNotificationPermission(): Promise<boolean> {
  const { status: existing } = await Notifications.getPermissionsAsync();
  if (existing === 'granted') return true;
  const { status } = await Notifications.requestPermissionsAsync();
  return status === 'granted';
}

export async function sendLocalAlert(title: string, body: string, severity: string) {
  const color = severity === 'critical' ? '#e76f51' : severity === 'warning' ? '#f4a261' : '#457b9d';
  await Notifications.scheduleNotificationAsync({
    content: { title, body, color },
    trigger: null,
  });
}

export function checkMoistureAlert(moisture: number | undefined, fieldName: string) {
  if (moisture !== undefined && moisture < 25) {
    sendLocalAlert(
      'Düşük Toprak Nemi',
      `${fieldName}: Toprak nemi %${moisture.toFixed(1)} - Sulama gerekebilir`,
      'warning',
    );
  }
}
