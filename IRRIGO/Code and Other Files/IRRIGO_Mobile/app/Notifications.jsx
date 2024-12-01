import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { FlatList, Image, RefreshControl, ScrollView, Text, View } from "react-native";
import tw from 'twrnc';

import { images } from "../constants";

const Notifications = () => {

  const onRefresh = async () => {
    setRefreshing(true)
    await refetch()
    setRefreshing(false)
  };

  return (
    <SafeAreaView style={tw`bg-primary h-full`}>
      <ScrollView style={tw`px-4 my-6`}>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Notifications;