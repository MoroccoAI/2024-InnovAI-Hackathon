#include <WiFi.h>

const char* ssid = ""; // Enter your Wi-Fi SSID here
const char* password = ""; // Enter your Wi-Fi password here
const char* server = "api.thingspeak.com";
const char* apiKey = ""; // Enter your ThingSpeak API key here
const int sensorPin = 2;    // Define your sensor pin here
const int valvePin = 25;    // Pin connected to the electrovalve
const int buttonPin = 26;   // Pin connected to the button
const int greenPin = 5;      // Pin connected to the LED green on
const int redPin = 16;      // pin for redpin connected to in 16
volatile long pulse;
bool valveState = LOW;
bool greenState = HIGH;       // State of the green led low
bool redState = LOW;     // Set thge state of red pin high
bool wifiConnected = false;
const float maxFlowRate = 2.0; // Maximum flow rate in liters per minute
const float pulsesPerLiter = 300; // Number of pulses per liter from the flow sensor

void setup() {
    pinMode(sensorPin, INPUT);
    pinMode(valvePin, OUTPUT);
    pinMode(buttonPin, INPUT_PULLUP); // Assuming the button is connected to ground when pressed
    pinMode(greenPin, OUTPUT);          // Set the green LED pin as output
    pinMode(redPin, OUTPUT);          // Set the red LED pin as output
    Serial.begin(115200);
    attachInterrupt(digitalPinToInterrupt(sensorPin), increase, RISING);
}

void loop() {
    static bool lastButtonState = HIGH;
    bool currentButtonState = digitalRead(buttonPin);

    // Check for a button state change from released to pressed
    if (lastButtonState == HIGH && currentButtonState == LOW) {
        // Button has been pressed, toggle the state of the valve and LED
        valveState = !valveState;

        // switch the to opposite if high go low if low go high
        greenState = !greenState;

        // set the state of red pin to opposite of green led
        redState = !greenState;
        
        // Update the pins based on the new states
        digitalWrite(valvePin, valveState);
        digitalWrite(greenPin, greenState);
        digitalWrite(redPin, redState);
        
        // Add a small delay to debounce the button
        delay(50);
    }
    
    // Update the last button state for the next loop iteration
    lastButtonState = currentButtonState;

    if (!wifiConnected){
     connectToWiFi(); 
    }

    // If connected to Wi-Fi, send data to ThingSpeak
    if (wifiConnected) {
        WiFiClient client;

        // Read the pulse count and reset it
        long pulseCount = pulse;
        pulse = 0;

        // Convert pulse count to flow rate
        float flowRate = pulseCount / pulsesPerLiter; // Calculate flow rate in liters

        // Print flow rate to Serial monitor for visualization
        Serial.print("Flow Rate: ");
        Serial.print(flowRate);
        Serial.println(" L/min");

        // Prepare the URL for the ThingSpeak update
        String url = "/update?api_key=";
        url += apiKey;!
        url += "&field1=";
        url += String(flowRate);

        if (client.connect(server, 80)) {
            // Send the HTTP request
            client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                         "Host: " + server + "\r\n" +
                         "Connection: close\r\n\r\n");

            // Wait for the response
            while (client.available()) {
                String line = client.readStringUntil('\r');
            }
            client.stop();
        }
        
    }
}

void increase() {
    pulse++; // Increment pulse when sensor event occurs
}

void connectToWiFi() {
    WiFi.begin(ssid, password);
    int attemptCount = 0;
    while (WiFi.status() != WL_CONNECTED && attemptCount < 10) {
        delay(500);
        attemptCount++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        wifiConnected = true;
    }
  }
