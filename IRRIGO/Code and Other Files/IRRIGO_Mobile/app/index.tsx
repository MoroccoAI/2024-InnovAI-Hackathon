import tw from 'twrnc';
import { StatusBar } from "expo-status-bar";
import { router } from "expo-router";
import { View, Text, Image, ScrollView, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

// You can replace this with your own images
import { images } from "../constants";

const Onboarding = () => {
  return (
    <SafeAreaView style={tw`bg-[#B5D1CD] h-full`}>
      <ScrollView
        contentContainerStyle={{
          height: "100%",
        }}
      >
        <View style={tw`w-full flex justify-center items-center h-full px-6`}>
          {/* Logo Image */}
          <Image
            source={images.irrigoLogo} // Replace with your IRRIGO logo
            style={tw`w-64 h-64 mb-4`}
            resizeMode="contain"
          />

          {/* Welcome Text */}
          <Text style={tw`text-3xl font-semibold text-gray-800 text-center mb-2`}>
            Welcome to
          </Text>
          <Text style={tw`text-3xl font-bold text-gray-800 text-center mb-8`}>
            IRRIGO
          </Text>

          {/* Tagline */}
          <Text style={tw`text-base text-gray-600 text-center mb-12`}>
            Every Irrigation for a Sustainable Future
          </Text>

          {/* Button with updated styling */}
          <TouchableOpacity
            onPress={() => router.push("/home")}
            style={tw`bg-[#B5D1CD] border-2 border-gray-600 p-4 rounded-full shadow-sm w-48 mt-auto mb-12`}
          >
            <Text style={tw`text-gray-800 text-center font-medium text-lg`}>
              Start
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      <StatusBar backgroundColor="#B5D1CD" style="dark" />
    </SafeAreaView>
  );
};

export default Onboarding;

