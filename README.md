# 💧 Irrigo: Smart Irrigation System for Water-Scarce Region

## 🚨 Problem  
Morocco is experiencing **increasing water stress**, with water availability dropping to less than **500 m³ per capita per year**, far below the **critical threshold of 1,700 m³ set by the WHO**. Key challenges include:  
- **Persistent droughts**.  
- **Unequal water resource distribution**.  
- **Inefficient irrigation practices**, causing both under- and over-irrigation.  

### 🌾 Case Study: Souss-Massa Region  
In Souss-Massa, a vital hub for Moroccan agriculture with **20,000 hectares of greenhouses exporting to Europe**:  
- **Groundwater levels are dropping 4.5 meters annually** due to overexploitation.  
- Farmers are forced to reduce operations or shut down, causing:  
  - Increased prices of fruits and vegetables.  
  - Threats to regional economic and environmental sustainability.  

---

## 🌱 Solution: Irrigo  

**Irrigo** is a **smart irrigation app mobile** designed to optimize water usage in Moroccan agriculture, especially in water-scarce regions like Souss-Massa. It integrates:  
- **IoT sensors and hardware**: For real-time monitoring.  
- **AI-powered recommendations**: For precise irrigation control.  
- **Mobile app and chatbot**: To assist farmers in sustainable practices about dry irrigation.  


## 📈 Impact  
**Irrigo** addresses water scarcity by:  
1. Ensuring crops receive only the necessary water, reducing waste.  
2. Decreasing dependency on fertilizers and pesticides.  
3. Promoting sustainable farming and increasing crop yields.


## 🛠️ Technical Architecture

### **Hardware Integration**

- **ESP32 Devices**: 
  - **Transmitter**: Collects sensor data and sends it via LoRa.  
  - **Server**: Connects to Firebase to retrieve recommendations.  
  - **Receiver**: Activates solenoid valves for irrigation.  
- **LoRa SX1278 Modules**: For wireless communication between ESP32 devices.  
- **Sensors**: Soil moisture, temperature (DHT11), and humidity.  
- **Solenoid Valves**: Controlled by the receiver ESP32 for irrigation.
  

### **Software Stack**

- **Arduino IDE**: Programming ESP32 devices.  
- **Firebase**: Cloud storage for irrigation recommendations.  
- **LoRa Libraries**: Communication protocol.  
- **Python Scripts**: Automate backend tasks (e.g., periodic updates on PythonAnywhere).  
- **Flask + ngrok**: API for chatbot and real-time recommendations.
  
### **IRRIGOClassifier system**
  ![image](https://github.com/user-attachments/assets/e47098ef-0d09-40c6-94a4-980761dbb63d)

### **IRRIGO CHAT**
<img width="608" alt="image" src="https://github.com/user-attachments/assets/551e85bc-540c-42e6-9cac-60bd5cf949bb">

---

## 📋 Implementation Details

### **Workflow**

1. **ESP32 Devices**:  
   - Transmitter collects real-time sensor data and sends it to the server ESP32 via LoRa.  
   - Server fetches irrigation recommendations from Firebase.  
   - Receiver receives instructions via LoRa and activates solenoid valves.  

2. **Data Flow**:  
   - **Sensor Data** → **ESP32 Transmitter** → **ESP32 Server** → **Firebase** → **ESP32 Receiver** → **Irrigation**
  ![image](https://github.com/user-attachments/assets/ed5b2a1e-a7ae-427c-b4c8-64287d0ea9e1)




3. **Automation**:  
   - Scripts on PythonAnywhere run periodically to update recommendations.
     ![image](https://github.com/user-attachments/assets/e4a4588e-f3bf-4440-9fda-a3584357276e)


---

## 📱 Mobile App Features



1. **Chatbot**:  
   - Real-time answers to questions like:  
     - "what are the advantages of dry irrigation?"  
     - "What’s the best irrigation technique?"  


2. **Dashboard**:  
   - Visualizes sensor data and weather forecasts.  
   - Displays AI-generated recommendations.

--

## 📊 how to run



# How to Run IRRIGO Mobile(Expo Frontend)

This guide will help you set up and run the **Expo-based React Native frontend** for IRRIGO .

---

## Prerequisites

Before starting, ensure you have the following installed:

1. **Node.js**: [Download and install](https://nodejs.org/).
2. **npm** (comes with Node.js) or **Yarn**: Install yarn with:
   ```bash
   npm install -g yarn
   ```
3. **Expo CLI**:
   - Install globally:
     ```bash
     npm install -g expo-cli
     ```

4. **Expo Go App** (for testing on physical devices):
   - Download for [Android](https://play.google.com/store/apps/details?id=host.exp.exponent) or [iOS](https://apps.apple.com/us/app/expo-go/id982107779).

---

## Install Dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

---

## Running the App

### 1. Start the Expo Server
Run the Expo development server:
```bash
expo start
```

This will open a terminal interface and a local web dashboard in your browser.

### 2. Test on a Device
- **Using Expo Go App**:
  - Scan the QR code displayed in the terminal or web dashboard.
  - Ensure your device and computer are on the same Wi-Fi network.
- **Using an Emulator/Simulator**:
  - For Android: Click **"Run on Android device/emulator"** on the Expo dashboard.
  - For iOS: Click **"Run on iOS simulator"** on the Expo dashboard (macOS only).

---


## Troubleshooting

### Common Issues

- **"Metro bundler failed to start"**:
  - Ensure no other apps are using the default port (19000).
  - Restart with:
    ```bash
    expo start --clear
    ```

- **Device Connection Issues**:
  - Ensure your computer and device are on the same network.
  - For physical devices, use the **Expo Go** app.





  
