import React, { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';


function AnaSayfa({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.baslik}>Akıllı Tarım Sistemine Hoş Geldiniz</Text>
      <Text style={styles.altBaslik}>Sistem Durumu: Aktif 🟢</Text>
      
      <TouchableOpacity 
        style={styles.buton} 
        onPress={() => navigation.navigate('Sera Kontrol')}
      >
        <Text style={styles.butonMetin}>Seraları Kontrol Et</Text>
      </TouchableOpacity>
    </View>
  );
}

// 2. EKRAN: Sera Kontrol Ekranı - DİNAMİK (STATE) VERSİYON
function SeraKontrol() {
  const [sicaklik, setSicaklik] = useState(24);
  const [nem, setNem] = useState(60);
  const [pompaAcik, setPompaAcik] = useState(false);

  const pompaKontrol = () => {
    if (pompaAcik) {
      setPompaAcik(false);
      setNem(nem - 15);
      setSicaklik(sicaklik + 2);
    } else {
      setPompaAcik(true);
      setNem(nem + 15);
      setSicaklik(sicaklik - 2);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.baslik}>1 Numaralı Sera</Text>
      
      <View style={styles.kart}>
        <Text style={styles.bilgiYazisi}>🌡 Sıcaklık: {sicaklik}°C</Text>
        <Text style={styles.bilgiYazisi}>💧 Nem Oranı: %{nem}</Text>
        <Text style={styles.bilgiYazisi}>☀️ Işık Seviyesi: Normal</Text>
        
        <View style={styles.cizgi} />

        <View style={styles.pompaAlani}>
          <Text style={styles.bilgiYazisi}>
            Su Pompası: {pompaAcik ? 'Aktif 🟢' : 'Kapalı 🔴'}
          </Text>
          
          <TouchableOpacity 
            style={[styles.kucukButon, { backgroundColor: pompaAcik ? '#d32f2f' : '#1976d2' }]} 
            onPress={pompaKontrol}
          >
            <Text style={styles.butonMetin}>
              {pompaAcik ? 'Pompayı Durdur' : 'Pompayı Çalıştır'}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

// Navigasyon Yönlendiricisi (Stack Navigator)
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="Ana Sayfa"
        screenOptions={{
          headerStyle: { backgroundColor: '#2e7d32' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen name="Ana Sayfa" component={AnaSayfa} />
        <Stack.Screen name="Sera Kontrol" component={SeraKontrol} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Arayüz Tasarım Ayarları (BİRLEŞTİRİLMİŞ CSS MANTIĞI)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  baslik: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
    textAlign: 'center',
  },
  altBaslik: {
    fontSize: 16,
    color: '#666',
    marginBottom: 30,
  },
  kart: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    elevation: 3, 
    shadowColor: '#000', 
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    width: '100%',
  },
  bilgiYazisi: {
    fontSize: 18,
    marginVertical: 10,
    color: '#444',
  },
  buton: {
    backgroundColor: '#2e7d32',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 8,
  },
  butonMetin: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  cizgi: {
    height: 1,
    backgroundColor: '#ccc',
    marginVertical: 15,
  },
  pompaAlani: {
    alignItems: 'center',
    marginTop: 10,
  },
  kucukButon: {
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 8,
    marginTop: 10,
  }
});
