import { StatusBar } from 'expo-status-bar';
import { KeyboardAvoidingView, Platform, ScrollView, Text, View } from 'react-native';
import { styles } from './App.styles';
import { Button } from './src/components/Button/index'

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

          <View style={styles}>
            <Button variant='primary' text={'Registrar-se'}></Button>
            <Button variant='primary' text={'Entrar'}></Button>
          </View>

          
        </View>

      </ScrollView>
    </KeyboardAvoidingView>
  );
}