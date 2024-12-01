import React, { useState, useEffect } from 'react';
import { SafeAreaView, ScrollView, Text, View, Image, ActivityIndicator } from 'react-native';
import tw from 'twrnc';
import * as Location from 'expo-location'; // Import expo-location
import moment from 'moment'; // To handle date and time formatting
import { wetherAPI } from '../../constants';

// Replace with your WeatherAPI key
const API_KEY = wetherAPI;

const Meteo = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);

  useEffect(() => {
    // Request permission and get current location
    const getLocation = async () => {
      try {
        // Request location permission
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          setError('Location permission denied');
          setLoading(false);
          return;
        }

        // Get current position
        let location = await Location.getCurrentPositionAsync({});
        const { latitude, longitude } = location.coords;
        setLatitude(latitude);
        setLongitude(longitude);
      } catch (err) {
        setError('Geolocation error');
        setLoading(false);
      }
    };

    getLocation();
  }, []);

  useEffect(() => {
    if (latitude && longitude) {
      // Fetch weather data using coordinates
      const fetchWeather = async () => {
        try {
          const response = await fetch(
            `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${latitude},${longitude}`
          );

          if (!response.ok) {
            throw new Error('HTTP error: ' + response.status);
          }

          const data = await response.json();
          setWeatherData(data);
        } catch (err) {
          setError('Error fetching weather data');
        } finally {
          setLoading(false);
        }
      };

      fetchWeather();
    }
  }, [latitude, longitude]);

  if (loading) {
    return (
      <SafeAreaView style={tw`bg-blue-100 h-full justify-center items-center`}>
        <ActivityIndicator size="large" color="#0000ff" />
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={tw`bg-blue-100 h-full justify-center items-center`}>
        <Text style={tw`text-red-500 font-semibold text-xl`}>{error}</Text>
      </SafeAreaView>
    );
  }

  // Format the current date and time
  const currentDateTime = moment().format('MMMM Do YYYY, h:mm:ss a');

  // Display weather data
  return (
    <SafeAreaView style={tw` h-full`}>
      <ScrollView style={tw`px-6 my-6`}>
        <Text style={tw`text-black text-4xl font-extrabold text-center mb-6`}>Weather</Text>

        {weatherData && (
          <View style={tw`bg-white p-6 rounded-lg shadow-md`}>
            {/* Display current date and time */}
            <Text style={tw`text-lg text-gray-600 text-center mb-4`}>{currentDateTime}</Text>

            {/* Weather information */}
            <Text style={tw`text-2xl font-semibold text-center text-gray-700`}>Location: {weatherData.location.name}</Text>
            <View style={tw`flex-row justify-center items-center mt-4`}>
              <Image
                source={{ uri: `https:${weatherData.current.condition.icon}` }}
                style={tw`w-20 h-20`}
              />
              <Text style={tw`text-6xl font-bold text-blue-600 ml-4`}>
                {weatherData.current.temp_c}°C
              </Text>
            </View>
            <Text style={tw`text-xl mt-4 text-center text-gray-600`}>
              Condition: {weatherData.current.condition.text}
            </Text>

            {/* Additional weather details */}
            <View style={tw`mt-6`}>
              <Text style={tw`text-xl text-gray-700`}>
                Wind: {weatherData.current.wind_kph} km/h
              </Text>
              <Text style={tw`text-xl text-gray-700 mt-2`}>
                Humidity: {weatherData.current.humidity}%
              </Text>
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

export default Meteo;
