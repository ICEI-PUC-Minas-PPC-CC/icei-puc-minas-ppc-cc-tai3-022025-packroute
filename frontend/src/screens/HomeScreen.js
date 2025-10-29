import React, { useEffect, useState, useRef } from 'react';
import { View, Text, TouchableOpacity, Alert } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';
import { styles } from '../styles/homeStyles';

export default function HomeScreen() {
  const [location, setLocation] = useState(null);
  const [region, setRegion] = useState(null);
  const mapRef = useRef(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permissão negada', 'O app precisa da sua localização.');
        return;
      }

      let current = await Location.getCurrentPositionAsync({});
      const initialRegion = {
        latitude: current.coords.latitude,
        longitude: current.coords.longitude,
        latitudeDelta: 0.01,
        longitudeDelta: 0.01,
      };
      setRegion(initialRegion);
      setLocation(current.coords);

      //Real time position
      const subscriber = await Location.watchPositionAsync(
        { accuracy: Location.Accuracy.High, distanceInterval: 5 },
        (loc) => {
          setLocation(loc.coords);
          setRegion((prev) => ({
            ...prev,
            latitude: loc.coords.latitude,
            longitude: loc.coords.longitude,
          }));
        }
      );

      return () => {
        subscriber.remove();
      };
    })();
  }, []);

  //Center map
  const handleCenterMap = () => {
    if (location && mapRef.current) {
      mapRef.current.animateToRegion({
        ...region,
        latitude: location.latitude,
        longitude: location.longitude,
      });
    }
  };

  const handleStartDeliveries = () => {
    Alert.alert('Rota iniciada!', 'Calculando a melhor rota para as entregas...');
  };

  return (
    <View style={styles.container}>
      {region ? (
        <MapView
          ref={mapRef}
          style={styles.map}
          region={region}
          showsUserLocation={true}
          followsUserLocation={true}
        >
          {location && (
            <Marker
              coordinate={{
                latitude: location.latitude,
                longitude: location.longitude,
              }}
              title="Você está aqui"
              pinColor="blue"
            />
          )}
        </MapView>
      ) : (
        <Text style={styles.loadingText}>Carregando mapa...</Text>
      )}

      <TouchableOpacity style={styles.centerButton} onPress={handleCenterMap}>
        <Text style={styles.buttonText}>📍</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.startButton} onPress={handleStartDeliveries}>
        <Text style={styles.startButtonText}>Iniciar Entregas</Text>
      </TouchableOpacity>
    </View>
  );
}
