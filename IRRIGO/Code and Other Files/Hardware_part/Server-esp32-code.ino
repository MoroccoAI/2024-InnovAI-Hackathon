

#include <WiFi.h>
#include <FirebaseESP32.h>
#include <LoRa.h>

// Wi-Fi configuration
#define WIFI_SSID "wifi name"
#define WIFI_PASSWORD " password"

// Firebase configuration
#define FIREBASE_HOST " http://quick-function-431210-h9.firebaseapp.com/"
#define FIREBASE_AUTH " quick-function-431210-h9"

// LoRa configuration
#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26

FirebaseData firebaseData;

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Wi-Fi connected!");

  // Initialize Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  // Initialize LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  Serial.println("LoRa initialized.");
}

void loop() {
  // Get recommendation from Firebase
  if (Firebase.getString(firebaseData, "/recommandation")) {
    String recommendation = firebaseData.stringData();
    Serial.println("Recommendation received: " + recommendation);
    sendLoRa(recommendation);
  }

  delay(5000);  // Check every 5 seconds
}

void sendLoRa(String data) {
  LoRa.beginPacket();
  LoRa.print(data);
  LoRa.endPacket();
  Serial.println("Recommendation sent via LoRa: " + data);
}
