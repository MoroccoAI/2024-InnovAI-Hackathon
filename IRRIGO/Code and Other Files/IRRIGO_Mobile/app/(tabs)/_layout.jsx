import { Image, Text, View, TouchableOpacity } from 'react-native';
import React from 'react';
import { Tabs, useRouter } from 'expo-router';
import tw from 'twrnc';
import { icons } from '../../constants';

const TabIcon = ({ icon, color, name, focused }) => {
  return (
    <View style={tw`flex items-center justify-center gap-2`}>
      <Image
        source={icon}
        resizeMode="contain"
        tintColor={color}
        style={tw`w-10 h-10`}
      />
      <Text style={tw`${focused ? "font-psemibold" : "font-pregular"} text-xs`}>
        {name}
      </Text>
    </View>
  );
};

// Composant pour les icônes dans l'en-tête
const HeaderIcons = () => {
  const router = useRouter(); // Pour naviguer vers d'autres pages

  return (
    <View style={tw`flex-row items-center gap-4 mr-4`}>
      {/* Icône de notification */}
      <TouchableOpacity onPress={() => router.push('/Notifications')}>
        <Image
          source={icons.notification} // Assurez-vous que l'icône existe
          style={tw`w-6 h-6`}
          resizeMode="contain"
        />
      </TouchableOpacity>

      {/* Icône de profil */}
      <TouchableOpacity onPress={() => router.push('/Profile')}>
        <Image
          source={icons.profile} // Assurez-vous que l'icône existe
          style={tw`w-6 h-6`}
          resizeMode="contain"
        />
      </TouchableOpacity>
    </View>
  );
};

const TabLayout = () => {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: "#E3EFEC",
        tabBarInactiveTintColor: "#CDCDE0",
        tabBarShowLabel: false,
        tabBarStyle: {
          backgroundColor: "#7EA497",
          borderTopWidth: 1,
          borderTopColor: "#E3EFEC",
          height: 80,
        },
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: "Home",
          headerShown: true,
          headerRight: () => <HeaderIcons />, // Ajout des icônes notification + profil
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={icons.home}
              color={color}
              focused={focused}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="chatbot"
        options={{
          title: "Chatbot",
          headerShown: true,
          headerRight: () => <HeaderIcons />,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={icons.chatbot}
              color={color}
              focused={focused}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="Sensors Data"
        options={{
          title: "Sensors Data",
          headerShown: true,
          headerRight: () => <HeaderIcons />,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={icons.sensors}
              color={color}
              focused={focused}
            />
          ),
        }}
      />
  
      <Tabs.Screen
        name="Weather"
        options={{
          title: "Weather",
          headerShown: true,
          headerRight: () => <HeaderIcons />,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={icons.meteo}
              color={color}
              focused={focused}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="history"
        options={{
          title: "Irrigation",
          headerShown: true,
          headerRight: () => <HeaderIcons />,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={icons.irrigation}
              color={color}
              focused={focused}
            />
          ),
        }}
      />
    </Tabs>
  );
};

export default TabLayout;
