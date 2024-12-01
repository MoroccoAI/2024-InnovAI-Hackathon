import React, { useState } from 'react';
import { View, Text, StyleSheet, useWindowDimensions } from 'react-native';
import { PieChart } from 'react-native-chart-kit';
import { LinearGradient } from 'expo-linear-gradient';
import DropDownPicker from 'react-native-dropdown-picker';

// Color palette
const CHART_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'];

const TEST_DATA = [
  { name: 'Food', amount: 300, color: '#FF6B6B', year: '2023', month: '11', week: '1' },
  { name: 'Transport', amount: 200, color: '#4ECDC4', year: '2024', month: '11', week: '1' },
  { name: 'Shopping', amount: 250, color: '#45B7D1', year: '2024', month: '11', week: '1' },
  { name: 'Entertainment', amount: 150, color: '#96CEB4', year: '2024', month: '9', week: '3' },
  { name: 'Groceries', amount: 180, color: '#FF6B6B', year: '2024', month: '9', week: '3' },
  { name: 'Utilities', amount: 120, color: '#4ECDC4', year: '2024', month: '10', week: '2' },
  { name: 'Healthcare', amount: 350, color: '#45B7D1', year: '2024', month: '10', week: '2' },
  { name: 'Education', amount: 200, color: '#96CEB4', year: '2024', month: '10', week: '2' },
  { name: 'Rent', amount: 1200, color: '#FF6B6B', year: '2024', month: '11', week: '1' },
  { name: 'Insurance', amount: 220, color: '#4ECDC4', year: '2024', month: '9', week: '3' },
  { name: 'Travel', amount: 500, color: '#45B7D1', year: '2024', month: '9', week: '3' },
  { name: 'Subscriptions', amount: 100, color: '#96CEB4', year: '2024', month: '10', week: '2' },
  { name: 'Dining Out', amount: 180, color: '#FF6B6B', year: '2024', month: '11', week: '1' }
];

const Chart = ({ data = null }) => {
  const { width } = useWindowDimensions();
  const displayData = data || TEST_DATA;


  // State to manage the selected filters
  const [selectedYear, setSelectedYear] = useState('2024');  // Default value set as a string
  const [selectedMonth, setSelectedMonth] = useState('11');  // Default value set as a string
  const [selectedWeek, setSelectedWeek] = useState('1');  // Default value set as a string

  // States to control dropdown visibility
  const [yearOpen, setYearOpen] = useState(false);
  const [monthOpen, setMonthOpen] = useState(false);
  const [weekOpen, setWeekOpen] = useState(false);

 // Filter data based on the selected year, month, and week
 const filteredData = displayData.filter(
  (item) =>
    item.year === selectedYear &&
    item.month === selectedMonth &&
    item.week === selectedWeek
);

 // Calculate the total amount based on filtered data
 const totalAmount = filteredData.reduce((sum, item) => sum + item.amount, 0);

 const chartData = filteredData.map(item => ({
   ...item,
   name: '',  // We don't need a name here for the pie chart
   legendFontSize: 12,
 }));
   // Check if there's no filtered data
   const noData = filteredData.length === 0;

  return (
    <View style={styles.container}>
      <View style={styles.filterContainer}>
        <View style={styles.dropdownRow}>
          {/* Year Dropdown */}
          <DropDownPicker
            open={yearOpen}
            value={selectedYear}
            items={[
              { label: '2024', value: '2024' },
              { label: '2023', value: '2023' }
            ]}
            setOpen={setYearOpen}
            setValue={setSelectedYear}
            style={styles.dropdown}
            containerStyle={styles.dropdownContainer}
            placeholder="Select Year"
            dropDownStyle={styles.dropdownStyle}
            labelStyle={styles.dropdownLabel}
          />

          {/* Month Dropdown */}
          <DropDownPicker
            open={monthOpen}
            value={selectedMonth}
            items={[
              { label: 'Nov', value: '11' },
              { label: 'Oct', value: '10' },
              { label: 'Sept', value: '9' }
            ]}
            setOpen={setMonthOpen}
            setValue={setSelectedMonth}
            style={styles.dropdown}
            containerStyle={styles.dropdownContainer}
            placeholder="Select Month"
            dropDownStyle={styles.dropdownStyle}
            labelStyle={styles.dropdownLabel}
          />

          {/* Week Dropdown */}
          <DropDownPicker
            open={weekOpen}
            value={selectedWeek}
            items={[
              { label: 'Week 1', value: '1' },
              { label: 'Week 2', value: '2' },
              { label: 'Week 3', value: '3' },
              { label: 'Week 4', value: '4' }
            ]}
            setOpen={setWeekOpen}
            setValue={setSelectedWeek}
            style={styles.dropdown}
            containerStyle={styles.dropdownContainer}
            placeholder="Select Week"
            dropDownStyle={styles.dropdownStyle}
            labelStyle={styles.dropdownLabel}
          />
        </View>
      </View>

      <View style={styles.card}>
        <LinearGradient colors={['#ffffff', '#f7f9fc']} style={styles.gradientBackground}>
          <Text style={styles.title}>Spending Overview</Text>
          <Text style={styles.subtitle}>Total: ${totalAmount}</Text>
          

          <View style={styles.chartContainer}>
            {noData ? (
              <Text style={styles.noDataText}>No data to display</Text>
            ) : (
              <PieChart
                data={chartData}
                width={width - 60}
                height={220}
                chartConfig={{
                  backgroundColor: '#fff',
                  backgroundGradientFrom: '#fff',
                  backgroundGradientTo: '#fff',
                  color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                }}
                accessor="amount"
                backgroundColor="transparent"
                center={[(width - 60) / 4, 0]}
                absolute
                hasLegend={false}
              />
            )}
          </View>


          <View style={styles.legendContainer}>
            {filteredData.map((item, index) => (
              <View key={index} style={styles.legendItem}>
                {/* Left side: Category */}
                <View style={styles.legendLeftSection}>
                  <View style={[styles.legendColor, { backgroundColor: item.color }]} />
                  <Text style={styles.legendCategoryText}>{item.name}</Text>
                </View>

                {/* Right side: Amount and Percentage */}
                <View style={styles.legendRightSection}>
                  <Text style={styles.legendAmountText}>${item.amount}</Text>
                  <Text style={styles.legendPercentageText}>
                    {((item.amount / totalAmount) * 100).toFixed(0)}%
                  </Text>
                </View>
              </View>
            ))}
          </View>
        </LinearGradient>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  dropdownRow: {
    flexDirection: 'row',  // Align items horizontally
    justifyContent: 'space-between',  // Space out the dropdowns
    flexWrap: 'wrap',  // Wrap dropdowns if they exceed screen width
  },
  dropdownContainer: {
    width: '33%',  // Adjust the width to fit within the row
    marginBottom: 15,
  },
  dropdown: {
    backgroundColor: '#ffffff',
    borderRadius: 8,
    borderColor: '#ddd',
    borderWidth: 1,
    paddingHorizontal: 10,
  },
  dropdownStyle: {
    backgroundColor: '#f0f0f0',
  },
  dropdownLabel: {
    fontSize: 16,
    color: '#333',
  },

  container: {
    width: '100%',
    alignItems: 'center',
    paddingHorizontal: 5,
    backgroundColor: '#fff',
  },
  card: {
    width: '100%',
    borderRadius: 20,
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  gradientBackground: {
    padding: 20,
    borderRadius: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2D3436',
    marginBottom: 4,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#636E72',
    marginBottom: 20,
    textAlign: 'center',
  },
  filterContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
 
  chartContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  legendContainer: {
    marginTop: 10,
  },
  legendItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  legendLeftSection: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  legendRightSection: {
    flexDirection: 'row',
    alignItems: 'center',
    minWidth: 120,
    justifyContent: 'flex-end',
  },
  legendColor: {
    width: 15,
    height: 15,
    borderRadius: 15,
    marginRight: 10,
  },
  legendCategoryText: {
    fontSize: 15,
    color: '#2D3436',
  },
  legendAmountText: {
    fontSize: 15,
    color: '#2D3436',
    marginRight: 15,
  },
  legendPercentageText: {
    fontSize: 14,
    color: '#636E72',
    minWidth: 35,
    textAlign: 'right',
  }
});

export default Chart;
