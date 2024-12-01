import React from 'react';
import { enableScreens } from 'react-native-screens';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Dashboard from './screens/Dashboard';
import Camera from './screens/Camera';
import InputScreen from './screens/input';

// Enable screens for better navigation performance
enableScreens();

// Create a stack navigator
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Dashboard">
        <Stack.Screen name="Dashboard" component={Dashboard} />
        <Stack.Screen 
          name="Camera" 
          component={Camera} 
          options={{ headerTitle: '' }}
        />
        <Stack.Screen name="Input" component={InputScreen}  options={{ headerTitle: 'Receipt' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}