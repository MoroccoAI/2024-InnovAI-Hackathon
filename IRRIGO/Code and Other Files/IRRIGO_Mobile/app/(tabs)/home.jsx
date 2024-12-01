import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { TouchableOpacity, Image, RefreshControl, ScrollView, Text, View } from "react-native";
import { router } from "expo-router";
import tw from 'twrnc';
import { ChevronRight } from "lucide-react-native";

import { images } from "../../constants";

const menuItems = [
  {
    id: 1,
    title: "Weather",
    image: images.Weather, // Replace with your weather image
    route: "/Weather"
  },
  {
    id: 2,
    title: "Sensors Data",
    image: images.sensors, // Replace with your sensors image
    route: "/Sensors Data"
  },
  {
    id: 3,
    title: "History of Irrigation",
    image: images.history, // Replace with your irrigation image
    route: "/history"
  }
];

const MenuItem = ({ title, image, onPress }) => (
  <TouchableOpacity 
    onPress={onPress}
    style={tw`flex-row items-center bg-white rounded-xl p-4 mb-4 shadow-sm`}
  >
    <Image
      source={image}
      style={tw`w-21 h-16  mr-4`}
      resizeMode="cover"
    />
    <Text style={tw`flex-1 text-gray-800 text-lg font-medium`}>{title}</Text>
    <ChevronRight size={24} color="#4A5568" />
  </TouchableOpacity>
);

const Home = () => {
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    // Add your refresh logic here
    setTimeout(() => setRefreshing(false), 1000);
  };

  return (
    <SafeAreaView style={tw`bg-[#E3EFEC] h-full`}>
      <ScrollView 
        style={tw`px-4 pt-6`}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <View style={tw`mb-8`}>
          <Text style={tw`text-gray-800 text-3xl font-bold mb-2`}>
            IRRIGO
          </Text>
          <Text style={tw`text-gray-600 text-base`}>
            Manage your irrigation intelligently
          </Text>
        </View>

        <View style={tw`mb-4`}>
          {menuItems.map((item) => (
            <MenuItem
              key={item.id}
              title={item.title}
              image={item.image}
              onPress={() => router.push(item.route)}
            />
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Home;

