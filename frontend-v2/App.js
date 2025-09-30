import { StatusBar } from 'expo-status-bar';
import { KeyboardAvoidingView, Platform, ScrollView, Text, View } from 'react-native';
import { Button } from './src/components/Button';
import { styles } from './App.styles';

export default function App() {
  return (

    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>

      <ScrollView style={styles.scrollView}>

        <View style={styles.content}>
          <StatusBar style="light" />
          
          <View style={styles.header}>
            <Text style={styles.title}>PackRoute</Text>
            <Text style={styles.subTitle}>Otimizador de entregas</Text>
          </View>

          
        </View>

      </ScrollView>
    </KeyboardAvoidingView>
  );
}