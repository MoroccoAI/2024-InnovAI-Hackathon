import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Text, Alert, FlatList, TouchableOpacity } from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import { MaterialIcons } from '@expo/vector-icons'; 
import DropDownPicker from 'react-native-dropdown-picker'; // Import DropDownPicker


const categories = ['Dairy', 'Breakfast', 'Sweets', 'Vegetables', 'Fruits']; // Hardcoded categories


const InputScreen = () => {

    const [items, setItems] = useState([{ name: '', cost: '', quantity: '', category:'' } ]);
    const [selectedCats, setSelectedCats] = useState([]); // Track selected category for each item
    const [openDropdowns, setOpenDropdowns] = useState([false]); // Track open state of each dropdown
     const [openStates, setOpenStates] = useState([false]); // State to track the open/close of each dropdown
     const [open, setOpen] = useState(false); // For controlling dropdown open/close

  
    const handleAddItem = () => {
      setItems([...items, { name: '', cost: '', quantity: '', category:''  }]);
      setSelectedCats([...selectedCats, categories[0]]);
      setOpenDropdowns([...openDropdowns, false]); // Add a new `false` entry to close the new dropdown
      setOpenStates([...openStates, false]);
    };
  
    const handleDropdownChange = (selectedItem, index) => {
        const newItems = [...items];
        newItems[index].category = selectedItem.value;
        setItems(newItems);
    
        // Update selected category for that item
        const updatedSelectedCats = [...selectedCats];
        updatedSelectedCats[index] = selectedItem.value;
        setSelectedCats(updatedSelectedCats);
      };
  
   

    const [date, setDate] = useState(new Date());
    const [receiptDate, setReceiptDate] = useState('');
    const [receiptTime, setReceiptTime] = useState('');
    

  const generateReceiptId = () => {
    const randomPart = Math.floor(1000 + Math.random() * 9000);
    return `${randomPart}`;
  };

  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showTimePicker, setShowTimePicker] = useState(false);

  const onDateChange = (event, selectedDate) => {
    const currentDate = selectedDate || date;
    setShowDatePicker(false);
    setDate(currentDate);
    setReceiptDate(currentDate.toISOString().split('T')[0]); // Format date as YYYY-MM-DD
  };



  const onTimeChange = (event, selectedTime) => {
    setShowTimePicker(false);
    if (selectedTime) {
      const formattedTime = selectedTime.toLocaleTimeString('en-GB'); // Format as HH:MM:SS
      setReceiptTime(formattedTime);
    }
  };

  const receiptId = generateReceiptId();


  // KeyExtractor to uniquely identify each item in the FlatList
  const keyExtractor = (item, index) => index.toString();

  const handleSubmit = () => {
    if (!receiptDate || !receiptTime) {
      Alert.alert('Error', 'Please provide both date and time for the receipt.');
      return;
    }

    const totalCost = items.reduce(
      (sum, item) => sum + parseFloat(item.cost || 0) * (item.quantity || 0),
      0
    );

    const receiptData = {
      receipt_id: receiptId,
      date: receiptDate,
      time: receiptTime,
      items,
      total_cost: totalCost.toFixed(2),
      currency: '£',
    };

    Alert.alert('Receipt Data', JSON.stringify(receiptData, null, 2));
    // Handle submission logic here (e.g., saving to a database or navigating back)
  };

  return (

<FlatList
        data={items}
        keyExtractor={keyExtractor}
        renderItem={({ item, index }) => (<View style={styles.container}>

        {/* Receipt Info */}
        {/* Date Picker */}

        
        <Text style={styles.subHeader}>Select Date & Time</Text>
      <TouchableOpacity
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          padding: 10,
          backgroundColor: '#f2f2f2',
          borderRadius: 8,
          marginBottom: 15,
        }}
        onPress={() => setShowDatePicker(true)}
      >
        <MaterialIcons name="calendar-today" size={24} color="#007AFF" />
        <Text style={{ marginLeft: 10, fontSize: 16 }}>
          {receiptDate || 'Tap to pick a date'}
        </Text>
      </TouchableOpacity>
         {/* Date Picker Modal */}
         {showDatePicker && (
        <DateTimePicker
          testID="dateTimePicker"
          value={date}
          mode="date"
          is24Hour={false}
          onChange={onDateChange}
          display="spinner"
        />
      )}


      {/* Time Picker */}
      <TouchableOpacity
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          padding: 10,
          backgroundColor: '#f2f2f2',
          borderRadius: 8,
        }}
        onPress={() => setShowTimePicker(true)}
      >
        <MaterialIcons name="access-time" size={24} color="#007AFF" />
        <Text style={{ marginLeft: 10, fontSize: 16 }}>
          {date.toLocaleTimeString() || 'Tap to pick a time'}
        </Text>
      </TouchableOpacity>

   
      {/* Time Picker Modal */}
      {showTimePicker && (
        <DateTimePicker
          testID="timePicker"
          value={date}
          mode="time"
          is24Hour={false}
          onChange={onTimeChange}
          display="spinner"
          minuteInterval={15}
        />
      )}



        {/* Items List */}
        <View style={styles.section}>
        <Text style={[styles.subHeader, { marginTop: 20 }]}>Items</Text>

          {items.map((item, index) => (
            <View key={index} style={styles.itemContainer}>
              <TextInput
                style={styles.input}
                placeholder="Item Name"
                value={item.name}
                onChangeText={(text) =>
                  setItems(items.map((itm, idx) => (idx === index ? { ...itm, name: text } : itm)))
                }
              />
              <TextInput
                style={styles.input}
                placeholder="Cost"
                keyboardType="numeric"
                value={item.cost}
                onChangeText={(text) =>
                  setItems(items.map((itm, idx) => (idx === index ? { ...itm, cost: text } : itm)))
                }
              />
              <TextInput
                style={styles.input}
                placeholder="Quantity"
                keyboardType="numeric"
                value={item.quantity}
                onChangeText={(text) =>
                  setItems(items.map((itm, idx) => (idx === index ? { ...itm, quantity: text } : itm)))
                }
              />


              
<DropDownPicker
            open={open}
            value={item.category}
            items={categories.map((category) => ({
              label: category,
              value: category,
            }))}
            setOpen={setOpen}
            setValue={(value) => {
              const newItems = [...items];
              newItems[index].category = value;
              setItems(newItems);
            }}
            placeholder="Select Category"
            style={styles.dropdown}
          />
            
              {/* <DropDownPicker
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
          /> */}
            
          </View>

            
           

            
          ))}
         <TouchableOpacity style={styles.addButton} onPress={handleAddItem}>
  <MaterialIcons name="add" size={24} color="#007AFF" />
  <Text style={styles.addButtonText}>Add Another Item</Text>
</TouchableOpacity>

        </View>

        {/* Submit Button */}
        <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
  <Text style={styles.submitButtonText}>Submit</Text>
</TouchableOpacity>

      </View>
     )}
     />
  );
};

const styles = StyleSheet.create({
  scrollContainer: {
    paddingVertical: 20,
    paddingHorizontal: 15,
  },
  container: { flex: 1, padding: 20, backgroundColor: '#f8f8f8' },
  header: { fontSize: 22, fontWeight: 'bold', marginBottom: 15, color: '#333' },
  section: { marginBottom: 20 },
  label: { fontSize: 16, fontWeight: 'bold', marginBottom: 5, color: '#555' },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 10,
    marginBottom: 10,
    borderRadius: 6,
    backgroundColor: '#fff',
  },
  generatedId: { fontSize: 14, color: '#777', marginTop: 10 },
  subHeader: { fontSize: 18, fontWeight: 'bold', marginBottom: 10, color: '#444' },
  itemContainer: { marginBottom: 15 },

  submitButton: {
    backgroundColor: '#007AFF',  // Button background color
    paddingVertical: 12,          // Vertical padding for a larger button
    paddingHorizontal: 20,        // Horizontal padding
    borderRadius: 8,             // Rounded corners
    alignItems: 'center',        // Center the text horizontally
    justifyContent: 'center',    // Center the text vertically
    marginTop: 20,               // Add margin on top (optional)
  },

  submitButtonText: {
    fontSize: 18,                // Font size for the button text
    fontWeight: 'bold',          // Make the text bold
    color: '#fff',               // White text color
  },
 



  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f2f2f2',  // Background color for the button
    paddingVertical: 10,          // Vertical padding for the button
    paddingHorizontal: 15,        // Horizontal padding for spacing
    borderRadius: 8,             // Rounded corners for the button
    marginBottom: 20,            // Margin at the bottom for spacing
    justifyContent: 'center',    // Center the items inside the button
  },

  addButtonText: {
    fontSize: 16,                // Font size for the text
    marginLeft: 10,              // Space between the icon and text
    color: '#007AFF',            // Text color
    fontWeight: 'bold',          // Bold text
  },
});

export default InputScreen;
