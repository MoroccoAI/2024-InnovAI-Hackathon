import React, { useState } from 'react';
import { 
  FlatList, 
  Text, 
  View, 
  TextInput, 
  TouchableOpacity, 
  KeyboardAvoidingView, 
  Platform 
} from "react-native";
import { SafeAreaView } from 'react-native-safe-area-context';
import Icon from 'react-native-vector-icons/Feather'; // Make sure to install this package
import tw from 'twrnc';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { id: 0, text: "How can i help you?", user: false }
  ]);
  const [inputText, setInputText] = useState('');
  const getRAGResponse = async (inputText) => {
    // Here you would typically make a call to your RAG backend
    
    try {
      const response = await fetch('http://dd63-34-30-132-9.ngrok-free.app/ask', { // Use your Flask server URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputText }),
      });
      

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
     

      console.log("#################################################",data.response,"#################################################");
      return data.response;
    }catch(e){
      alert("error is ",e,"######");
      console.log(e);
    }
  }

  const handleSend = async () => {
    if (inputText.trim() === '') return;

    // Add user message
    const userMessage = { id: messages.length, text: inputText, user: true };
    setMessages([...messages, userMessage]);

    // Here you would typically make a call to your RAG backend
    // For now, we'll simulate a response
    const response = await getRAGResponse(inputText);
    const botMessage = { 
      id: messages.length + 1, 
      text: response, 
      user: false 
    };
    setMessages(prevMessages => [...prevMessages, botMessage]);
    

    setInputText('');
  };

  const renderMessage = ({ item }) => (
    <View 
      style={[
        tw`rounded-2xl px-4 py-3 my-1 max-w-[85%]`,
        item.user 
          ? tw`self-end bg-[#e8e8e8]` 
          : tw`self-start bg-[#d7ede3]`,
      ]}
    >
      {!item.user && item.id === 0 && (
        <TouchableOpacity style={tw`absolute -left-6 top-3`}>
          <Icon name="paperclip" size={20} color="#666" />
        </TouchableOpacity>
      )}
      <Text style={tw`text-black text-base`}>{item.text}</Text>
    </View>
  );

  return (
    <SafeAreaView style={tw`bg-[#f0f7f4] h-full`}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={tw`flex-1`}
      >
        <View style={tw`px-8 py-6 flex-1`}>
          <FlatList
            data={messages}
            renderItem={renderMessage}
            keyExtractor={item => item.id.toString()}
            style={tw`flex-1`}
            contentContainerStyle={tw`pb-4`}
          />
        </View>
        <View style={tw`px-8 pb-6`}>
          <View style={tw`flex-row items-center bg-white rounded-full shadow-sm border border-gray-100`}>
            <TextInput
              style={tw`flex-1 px-6 py-3 text-base`}
              value={inputText}
              onChangeText={setInputText}
              placeholder="Écrivez votre message..."
              placeholderTextColor="#666"
              multiline
            />
            <TouchableOpacity 
              style={tw`pr-4 pl-2`}
              onPress={handleSend}
            >
              <Icon name="send" size={24} color="#666" />
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default Chatbot;