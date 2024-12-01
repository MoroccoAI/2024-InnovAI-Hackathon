#include <LoRa.h>

// LoRa configuration
#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26

void setup() {
  Serial.begin(115200);

  // Initialize LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  Serial.println("LoRa initialized.");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedData = "";
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    Serial.println("Data received via LoRa: " + receivedData);

    // Handle the received recommendation to trigger solenoid valves
    triggerIrrigation(receivedData);
  }
}

void triggerIrrigation(String recommendation) {
  // Implement logic to trigger solenoid valve based on the received recommendation
  Serial.println("Triggering irrigation based on recommendation: " + recommendation);
}
