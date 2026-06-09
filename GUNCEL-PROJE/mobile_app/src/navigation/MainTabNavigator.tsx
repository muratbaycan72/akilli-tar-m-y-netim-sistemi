import React from 'react';
import { Text } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/home/HomeScreen';
import SensorsStack from './SensorsStack';
import IrrigationScreen from '../screens/operations/IrrigationScreen';
import AlertsScreen from '../screens/alerts/AlertsScreen';
import SettingsScreen from '../screens/settings/SettingsScreen';
import { colors } from '../utils/theme';
import type { RootTabParamList } from './types';

const Tab = createBottomTabNavigator<RootTabParamList>();

const TAB_ICONS: Record<string, string> = {
  Home: '🏠',
  Sensors: '📡',
  Operations: '💧',
  Alerts: '🔔',
  Settings: '⚙️',
};

export default function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerStyle: { backgroundColor: colors.primaryDark },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: '600' },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: colors.border,
          paddingBottom: 4,
          height: 60,
        },
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
        tabBarIcon: ({ focused }) => (
          <Text style={{ fontSize: focused ? 22 : 20, opacity: focused ? 1 : 0.6 }}>
            {TAB_ICONS[route.name]}
          </Text>
        ),
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: 'Ana Sayfa', headerTitle: 'Akıllı Tarım' }} />
      <Tab.Screen name="Sensors" component={SensorsStack} options={{ title: 'Sensörler', headerShown: false }} />
      <Tab.Screen name="Operations" component={IrrigationScreen} options={{ title: 'Sulama' }} />
      <Tab.Screen name="Alerts" component={AlertsScreen} options={{ title: 'Alarmlar' }} />
      <Tab.Screen name="Settings" component={SettingsScreen} options={{ title: 'Ayarlar' }} />
    </Tab.Navigator>
  );
}
