import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import SensorListScreen from '../screens/sensors/SensorListScreen';
import SensorDetailScreen from '../screens/sensors/SensorDetailScreen';
import { colors } from '../utils/theme';
import type { SensorsStackParamList } from './types';

const Stack = createNativeStackNavigator<SensorsStackParamList>();

export default function SensorsStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: colors.primaryDark },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: '600' },
      }}
    >
      <Stack.Screen name="SensorList" component={SensorListScreen} options={{ title: 'Sensörler' }} />
      <Stack.Screen name="SensorDetail" component={SensorDetailScreen} options={{ title: 'Sensör Detayı' }} />
    </Stack.Navigator>
  );
}
