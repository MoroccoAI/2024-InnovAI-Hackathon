import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { FlatList, RefreshControl, ScrollView, Text, TouchableOpacity, View } from "react-native";
import tw from 'twrnc';
import Icon from 'react-native-vector-icons/Ionicons'; // Assurez-vous d'installer cette bibliothèque

const Profile = () => {
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    // Simulez un rafraîchissement (remplacez par une API ou autre logique)
    setTimeout(() => setRefreshing(false), 1000);
  };

  return (
    <SafeAreaView style={tw`bg-primary h-full`}>
      <ScrollView 
        style={tw`px-4 my-6`} 
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >

        {/* Carte du profil */}
        <View style={tw`bg-white rounded-lg shadow-md p-4 mb-6`}>
          <View style={tw`flex-row items-center`}>
            <Icon name="person-circle-outline" size={48} color="#6C7A89" />
            <View style={tw`ml-4`}>
              <Text style={tw`text-black text-lg font-psemibold`}>Nom d'utilisateur</Text>
              <Text style={tw`text-gray-500 text-sm`}>user.email@example.com</Text>
            </View>
          </View>
        </View>

        {/* Liste des options */}
        <View style={tw`bg-white rounded-lg shadow-md`}>
          <TouchableOpacity style={tw`flex-row items-center p-4 border-b border-gray-200`}>
            <Icon name="call-outline" size={20} color="#6C7A89" />
            <Text style={tw`ml-4 text-black`}>Téléphone</Text>
          </TouchableOpacity>

          <TouchableOpacity style={tw`flex-row items-center p-4 border-b border-gray-200`}>
            <Icon name="notifications-outline" size={20} color="#6C7A89" />
            <Text style={tw`ml-4 text-black`}>Notification</Text>
          </TouchableOpacity>

          <TouchableOpacity style={tw`flex-row items-center p-4 border-b border-gray-200`}>
            <Icon name="mail-outline" size={20} color="#6C7A89" />
            <Text style={tw`ml-4 text-black`}>Email</Text>
          </TouchableOpacity>

          <TouchableOpacity style={tw`flex-row items-center p-4 border-b border-gray-200`}>
            <Icon name="help-circle-outline" size={20} color="#6C7A89" />
            <Text style={tw`ml-4 text-black`}>Aide</Text>
          </TouchableOpacity>

          <TouchableOpacity style={tw`flex-row items-center p-4`}>
            <Icon name="log-out-outline" size={20} color="#6C7A89" />
            <Text style={tw`ml-4 text-black`}>Déconnecter</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Profile;
