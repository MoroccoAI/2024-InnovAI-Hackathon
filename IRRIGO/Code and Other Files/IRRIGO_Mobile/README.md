

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


