transmitter ESP32 Code
#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>

// Pins
#define DHTPIN 4 // Pin pour le DHT11
#define DHTTYPE DHT11
#define SOIL_SENSOR_PIN 34 
// LoRa
#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);

  // Initialisation du DHT
  dht.begin();
  Serial.println("DHT11 initialisé.");

  // Initialisation LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(433E6)) {
    Serial.println("Erreur de démarrage LoRa !");
    while (1);
  }
  Serial.println("LoRa initialisé.");
}

void loop() {
  // Lecture des données
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilMoisture = analogRead(SOIL_SENSOR_PIN);
  float soilPercentage = map(soilMoisture, 0, 4095, 0, 100); // Conversion en %

  // Vérifier les erreurs de lecture
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Erreur de lecture DHT !");
    return;
  }

  // Création du message
  String message = String("{\"temperature\":") + temperature + 
                   ",\"humidity\":" + humidity +
                   ",\"soilMoisture\":" + soilPercentage + "}";

  // Envoi via LoRa
  LoRa.beginPacket();
  LoRa.print(message);
  LoRa.endPacket();

  Serial.println("Données envoyées : " + message);
  delay(5000); // Pause de 5 secondes
}

