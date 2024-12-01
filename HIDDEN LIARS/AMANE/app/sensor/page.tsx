"use client";

import React, { useEffect, useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Thermometer, Droplet, Activity } from "lucide-react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  TimeScale,
} from "chart.js";
import "chartjs-adapter-date-fns";

// Registering Chart.js components
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, TimeScale);

// Chart data interface
interface ChartDataState {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    tension: number;
  }[];
}

const SensorPage: React.FC = () => {
  // State variables
  const [currentTemperature, setCurrentTemperature] = useState<number | null>(null);
  const [currentHumidity, setCurrentHumidity] = useState<number | null>(null);
  const [currentConductivity, setCurrentConductivity] = useState<number | null>(null);

  const previousTemperatureRef = useRef<number | null>(null);

  const [chartData, setChartData] = useState<ChartDataState>({
    labels: [],
    datasets: [
      {
        label: "Temperature",
        data: [],
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        tension: 0.3,
      },
      {
        label: "Humidity",
        data: [],
        borderColor: "rgba(192, 75, 192, 1)",
        backgroundColor: "rgba(192, 75, 192, 0.2)",
        tension: 0.3,
      },
      {
        label: "Conductivity",
        data: [],
        borderColor: "rgba(192, 192, 75, 1)",
        backgroundColor: "rgba(192, 192, 75, 0.2)",
        tension: 0.3,
      },
    ],
  });

  // Function to update chart data
  const updateChartData = (value: number, datasetIndex: number) => {
    setChartData((prevState) => {
      const newLabels = [...prevState.labels, new Date().toLocaleTimeString()];
      const updatedDatasets = prevState.datasets.map((dataset, index) => {
        if (index === datasetIndex) {
          const newData = [...dataset.data, value].slice(-10); // Keep only the last 10 data points
          return { ...dataset, data: newData };
        }
        return dataset;
      });

      return {
        labels: newLabels.slice(-10), // Keep only the last 10 labels
        datasets: updatedDatasets,
      };
    });
  };

  // useEffect to handle EventSource streams
  useEffect(() => {
    const temperatureSource = new EventSource(
      "https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net/start_temp_simulation"
    );

    temperatureSource.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      const value = Math.round(parsedData.temperature);
      setCurrentTemperature(value);
      updateChartData(value, 0); // Update the first dataset (Temperature)
    };

    const humiditySource = new EventSource(
      "https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net/start_humidity_simulation"
    );

    humiditySource.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      const value = Math.round(parsedData.humidity);
      setCurrentHumidity(value);
      updateChartData(value, 1); // Update the second dataset (Humidity)
    };

    const conductivitySource = new EventSource(
      "https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net/start_conductivity_simulation"
    );

    conductivitySource.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      const value = Math.round(parsedData.conductivity);
      setCurrentConductivity(value);
      updateChartData(value, 2); // Update the third dataset (Conductivity)
    };

    return () => {
      temperatureSource.close();
      humiditySource.close();
      conductivitySource.close();
    };
  }, []);

  // Component rendering
  return (
    <div>
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Temperature Overview</CardTitle>
              <Thermometer className="h-6 w-6 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {currentTemperature !== null ? `${currentTemperature} °C` : "Waiting for data..."}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Humidity Overview</CardTitle>
              <Droplet className="h-6 w-6 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {currentHumidity !== null ? `${currentHumidity} %` : "Waiting for data..."}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Conductivity Overview</CardTitle>
              <Activity className="h-6 w-6 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {currentConductivity !== null ? `${currentConductivity} µS/cm` : "Waiting for data..."}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="bg-white shadow-md rounded-lg p-4">
        <Line
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                title: {
                  display: true,
                  text: 'Sensor Data Over Time',
                  font: {
                    size: 16,
                  },
                },
                legend: {
                  display: true, 
                  position: "top", 
                  labels: {
                    font: {
                      size: 12,
                    },
                    color: "#333",
                  },
                },
                tooltip: {
                  mode: 'index',
                  intersect: false,
                },
              },
              scales: {
                x: {
                  display: true,
                  title: {
                    display: true,
                    text: 'Time',
                  },
                  grid: {
                    display: true,
                  },
                },
                y: {
                  display: true,
                  title: {
                    display: true,
                    text: 'Value',
                  },
                  beginAtZero: true,
                  grid: {
                    display: true,
                  },
                },
              },
            }}
            height={400}
          />

        </div>
      </div>
    </div>
  );
};

export default SensorPage;
