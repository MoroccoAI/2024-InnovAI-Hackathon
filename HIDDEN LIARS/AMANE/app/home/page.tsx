"use client";

import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import IrrigationStatusCards from "../components/IrrigationStatus";

export default function HomePage() {
  const [weatherSummary, setWeatherSummary] = useState({
    totalRain: 0,
    avgHumidity: 0,
    avgEvapotranspiration: 0,
  });

  const [sensorData, setSensorData] = useState({
    humidity: 0,
    conductivity: 0,
    env_humidity: 0,
    env_temperature: 0,
    temperature: 0,
  });

  const [receivedSensors, setReceivedSensors] = useState<Record<string, boolean>>({
    humidity: false,
    conductivity: false,
    env_humidity: false,
    env_temperature: false,
    temperature: false,
  });

  const [modelResponse, setModelResponse] = useState("");
  const [dataCollectionPaused, setDataCollectionPaused] = useState(false);

  const baseUrl =
    "https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net";

  const prepareModelData = useCallback(() => ({
    features: [
      sensorData.conductivity,
      sensorData.humidity,
      sensorData.temperature,
      sensorData.env_humidity,
      sensorData.env_temperature,
      weatherSummary.totalRain,
      weatherSummary.avgHumidity,
      weatherSummary.avgEvapotranspiration,
    ],
  }), [sensorData, weatherSummary]);

  const sendDataToModel = useCallback(async () => {
    const url = `${baseUrl}/predict_irrigation`;
    const data = prepareModelData();

    try {
      const response = await axios.post(url, data);
      setModelResponse(response.data.message || "No response message provided.");
    } catch (error) {
      console.error("Error sending data to the model:", error);
      setModelResponse("An error occurred while communicating with the model.");
    }
  }, [prepareModelData]);

  useEffect(() => {
    const sensorEndpoints = [
      { endpoint: "/start_humidity_simulation", key: "humidity" },
      { endpoint: "/start_conductivity_simulation", key: "conductivity" },
      { endpoint: "/start_env_humidity_simulation", key: "env_humidity" },
      { endpoint: "/start_env_temperature_simulation", key: "env_temperature" },
      { endpoint: "/start_temp_simulation", key: "temperature" },
    ];

    const handleSensorData = (key: string, value: number) => {
      setSensorData((prev) => ({ ...prev, [key]: value }));
      setReceivedSensors((prev) => ({ ...prev, [key]: true }));
    };

    const startEventSources = () => {
      const sources = sensorEndpoints.map(({ endpoint, key }) => {
        const source = new EventSource(`${baseUrl}${endpoint}`);

        source.onmessage = (event) => {
          try {
            const parsedData = JSON.parse(event.data);
            const value = parsedData[key];

            if (value !== undefined && !isNaN(Number(value))) {
              console.log(`Received data for ${key}:`, value);
              handleSensorData(key, Math.round(Number(value)));
            }
          } catch (error) {
            console.error(`Error processing data from ${endpoint}:`, error);
          }
        };

        source.onerror = (error) => {
          console.error(`Error with EventSource for ${endpoint}:`, error);
          source.close();
        };

        return source;
      });

      return sources;
    };

    const fetchWeatherData = async () => {
      const params = {
        latitude: 33.5625,
        longitude: -7.625,
        hourly: ["relative_humidity_2m", "rain", "et0_fao_evapotranspiration"],
        forecast_days: 3,
      };
      const url = "https://api.open-meteo.com/v1/forecast";

      try {
        const response = await axios.get(url, { params });
        const hourly = response.data.hourly;

        const totalRain = hourly.rain.reduce((sum: number, value: number) => sum + value, 0);
        const avgHumidity =
          hourly.relative_humidity_2m.reduce((sum: number, value: number) => sum + value, 0) /
          hourly.relative_humidity_2m.length;
        const avgEvapotranspiration =
          hourly.et0_fao_evapotranspiration.reduce((sum: number, value: number) => sum + value, 0) /
          hourly.et0_fao_evapotranspiration.length;

        setWeatherSummary({
          totalRain: Number(totalRain.toFixed(2)),
          avgHumidity: Number(avgHumidity.toFixed(2)),
          avgEvapotranspiration: Number(avgEvapotranspiration.toFixed(2)),
        });
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    };

    const startDataCollection = () => {
      if (!dataCollectionPaused) {
        console.log("Starting data collection...");
        fetchWeatherData();
        const sources = startEventSources();

        const interval = setInterval(() => {
          const allSensorsReceived = Object.values(receivedSensors).every(Boolean);

          if (allSensorsReceived) {
            console.log("All sensor data received. Sending data to the model...");

            // Send data to the model
            sendDataToModel();

            // Pause for an hour
            setDataCollectionPaused(true);
            sources.forEach((source) => source.close());
            clearInterval(interval);

            setTimeout(() => {
              console.log("Resuming data collection...");
              setReceivedSensors({
                humidity: false,
                conductivity: false,
                env_humidity: false,
                env_temperature: false,
                temperature: false,
              });
              setDataCollectionPaused(false);
            }, 60 * 60 * 1000); // 1 hour
          }
        }, 1000);
      }
    };

    startDataCollection();

    return () => {
      setDataCollectionPaused(true);
    };
  }, [sendDataToModel, receivedSensors]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Weather and Sensor Data</h1>

      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl font-semibold mb-2">Weather Summary (Next 3 Days)</h2>
          <p>Total Rain: {weatherSummary.totalRain} mm</p>
          <p>Average Humidity: {weatherSummary.avgHumidity}%</p>
          <p>Average Evapotranspiration: {weatherSummary.avgEvapotranspiration} mm</p>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-2">Sensor Readings</h2>
          <p>Current Humidity: {sensorData.humidity}%</p>
          <p>Current Conductivity: {sensorData.conductivity}</p>
          <p>Environment Temperature: {sensorData.env_temperature}°C</p>
          <p>Environment Humidity: {sensorData.env_humidity}%</p>
          <p>Soil Temperature: {sensorData.temperature}°C</p>
        </div>
      </div>

      <IrrigationStatusCards modelResponse={modelResponse} />
    </div>
  );
}
