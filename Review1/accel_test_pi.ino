#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <WiFi.h>

const char* ssid = "YOUR SSID";
const char* password = "SSID PASSWORD";
const char* host = "HOST IP ADDRESS"; // Raspberry Pi IP address

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Send accelerometer data to Raspberry Pi
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    if (client.connect(host, 80)) {
      String data = String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z);
      client.print(data);
      delay(10);
    }
    client.stop();
  }
  delay(100); // Adjust delay as needed
}
