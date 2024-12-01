import React from 'react';
import { View, Text, StyleSheet, useWindowDimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import Ionicons from 'react-native-vector-icons/Ionicons';  // Import the icon library


const TEST_DATA = {
  actual: [
    { month: 'Apr', amount: 750 },
    { month: 'May', amount: 900 },
    { month: 'Jun', amount: 800 },
    { month: 'Jul', amount: 850 },
    { month: 'Aug', amount: 950 },
    { month: 'Sep', amount: 1000 },
    { month: 'Oct', amount: 880 },
    { month: 'Nov', amount: 920 }
  ]
};

const PREDICTION_DATA = [
  { month: 'Apr', amount: 760 },
  { month: 'May', amount: 870 },
  { month: 'Jun', amount: 800 },
  { month: 'Jul', amount: 840 },
  { month: 'Aug', amount: 930 },
  { month: 'Sep', amount: 999 },
  { month: 'Oct', amount: 870 },
  { month: 'Nov', amount: 930 },
  { month: 'Dec', amount: 966 }
];

const CHART_COLORS = ['#4E7BEC', '#52C49B']; // Colors for actual and predicted data

const SpendingTrend = ({ data = null }) => {
  const { width } = useWindowDimensions();
  const displayData = data || TEST_DATA; // Use passed data or default to TEST_DATA
  const totalActual = displayData.actual.reduce((sum, item) => sum + item.amount, 0); // Total of actual data

  const predictionData = PREDICTION_DATA; // Always use PREDICTION_DATA for predictions

  // Prepare the chart data by extracting months and amounts
  const labels = displayData.actual.map(d => d.month); // Get months from actual data
  const actualAmounts = displayData.actual.map(d => d.amount); // Get actual amounts
  const predictionAmounts = predictionData.map(d => d.amount); // Get prediction amounts

  // Create datasets based on whether actual and predicted values are equal
  const actualDataset = {
    data: actualAmounts,
    color: (opacity = 1) => CHART_COLORS[0], // Color for actual data
    strokeWidth: 2
  };

  const predictedDataset = {
    data: predictionAmounts,
    color: (opacity = 1) => CHART_COLORS[1], // Color for predicted data
    strokeWidth: 2,
    strokeDasharray: [5, 5] // Dashed line for predictions
  };

  // Modify the chart data to only include the predicted line if actual != predicted
  const filteredDatasets = actualAmounts.map((actual, index) => {
    // If the actual value equals the predicted value, don't add the predicted line for that month
    if (actual === predictionAmounts[index]) {
      return [actualDataset]; // Only add the actual dataset
    }
    return [actualDataset, predictedDataset]; // Both datasets if actual != predicted
  });

  const chartData = {
    labels: labels, // Display actual months (no need to manually add 'Dec' here)
    datasets: filteredDatasets[0] // Start with first entry for datasets
  };

  // Define the legend items with dollar units
  const legendItems = [
    { name: 'Actual', color: CHART_COLORS[0], amount: `$${totalActual}` }, // Add $ symbol to actual amount
    { name: 'Predicted (n+1)', color: CHART_COLORS[1], amount: `$${PREDICTION_DATA[8].amount}` } // Add $ symbol to predicted amount
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Spending Trend</Text>
      <LineChart
        data={chartData}
        width={width - 40}
        height={220}
        chartConfig={{
          backgroundColor: '#fff',
          backgroundGradientFrom: '#fff',
          backgroundGradientTo: '#fff',
          decimalPlaces: 0,
          color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(45, 52, 54, ${opacity})`,
          propsForLabels: {
            fontSize: 12,
          },
          propsForDots: {
            r: '4',
            strokeWidth: '2',
            stroke: '#fff',
          },
        }}
        withInnerLines={false}
        withDots={true}
        withShadow={false}
        bezier
        style={styles.chart}
      />
      
      {/* Display the legend */}
      <View style={styles.legendContainer}>
        {legendItems.map((item, index) => (
          <View key={index} style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: item.color }]} />
            <Text style={styles.legendText}>{item.name}: {item.amount}</Text>
          </View>
        ))}




      </View>
       {/* AI Suggested Spending Advice */}
    <View style={styles.aiAdvice}>
      <Ionicons name="bulb" size={25} color="#FBC02D" style={styles.icon} /> {/* Yellow Icon */}
      <Text style={styles.aiText}>AI Suggested Spending Advice: {"Based on your trends, consider reducing spending in October for better savings."}</Text>
    </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  chart: {
    borderRadius: 8,
  },
  legendContainer: {
    marginTop: 30,
    flexDirection: 'column', // Stack the items vertically
    alignItems: 'flex-start', // Align the legend items to the left
    paddingLeft: 30, // Optional: Add some left padding if needed for spacing
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 5, // Add some space between the items
  },
  legendColor: {
    width: 20,
    height: 20,
    borderRadius: 5,
    marginRight: 5,
  },
  legendText: {
    fontSize: 14,
    color: '#333',
  },
  aiAdvice: {
    backgroundColor: '#f5f5f5',  // Light gray background
    padding: 10,
    marginTop: 60,
    borderRadius: 5,
    fontSize: 14,
    color: '#333',
    borderWidth: 1,
    borderColor: '#ddd',
    textAlign: 'center',
    flexDirection: 'column',  // Stack the icon and text vertically
    alignItems: 'center',  // Center the icon and text
  },
  
  icon: {
    marginBottom: 10,  // Space between the icon and the text
  },
  
  aiText: {
    fontSize: 14,  // Smaller font size for the text
    color: '#333',  // Darker text for better readability
    textAlign: 'center',
  },
  
  

});

export default SpendingTrend;
