/*
====================================================
   Inspire Project - Smart Soil Analyzer
   Board : ESP32
====================================================
*/
#include "sdkconfig.h"
#if CONFIG_ESP_WIFI_REMOTE_ENABLED
#error "WiFiProv is only supported in SoCs with native Wi-Fi support"
#endif
#include <WiFiProv.h>
#include <nvs_flash.h>
#include <WiFiAP.h>
#include "BluetoothSerial.h"
#include <HTTPClient.h>

const char* serverURL = "http://192.168.31.79:5000/sensor";

BluetoothSerial SerialBT;

// #define USE_SOFT_AP // Uncomment if you want to enforce using the Soft AP method instead of BLE
const char *pop = "abcd1234";           // Proof of possession - otherwise called a PIN - string provided by the device, entered by the user in the phone app
const char *service_name = "PROV_Soil_Sathi";  // Name of your device (the Espressif apps expects by default device name starting with "Prov_")
const char *service_key = NULL;         // Password used for SofAP method (NULL = no password needed)
bool reset_provisioned = false;          // When true the library will automatically delete previously provisioned data.

// WARNING: SysProvEvent is called from a separate FreeRTOS task (thread)!
void SysProvEvent(arduino_event_t *sys_event) {
  switch (sys_event->event_id) {
    case ARDUINO_EVENT_WIFI_STA_GOT_IP:
      Serial.print("\nConnected IP address : ");
      Serial.println(IPAddress(sys_event->event_info.got_ip.ip_info.ip.addr));
      break;
    case ARDUINO_EVENT_WIFI_STA_DISCONNECTED: Serial.println("\nDisconnected. Connecting to the AP again... "); break;
    case ARDUINO_EVENT_PROV_START:            Serial.println("\nProvisioning started\nGive Credentials of your access point using smartphone app"); break;
    case ARDUINO_EVENT_PROV_CRED_RECV:
    {
      Serial.println("\nReceived Wi-Fi credentials");
      Serial.print("\tSSID : ");
      Serial.println((const char *)sys_event->event_info.prov_cred_recv.ssid);
      Serial.print("\tPassword : ");
      Serial.println((char const *)sys_event->event_info.prov_cred_recv.password);
      break;
    }
    case ARDUINO_EVENT_PROV_CRED_FAIL:
    {
      Serial.println("\nProvisioning failed!\nPlease reset to factory and retry provisioning\n");
      if (sys_event->event_info.prov_fail_reason == NETWORK_PROV_WIFI_STA_AUTH_ERROR) {
        Serial.println("\nWi-Fi AP password incorrect");
      } else {
        Serial.println("\nWi-Fi AP not found....Add API \" nvs_flash_erase() \" before beginProvision()");
      }
      break;
    }
    case ARDUINO_EVENT_PROV_CRED_SUCCESS: Serial.println("\nProvisioning Successful"); break;
    case ARDUINO_EVENT_PROV_END:          Serial.println("\nProvisioning Ends"); break;
    default:                              break;
  }
}
const int PH_PIN = 34;
const int MOISTURE_PIN = 4;
String mode = "none";
const int NUM_SAMPLES = 20;

// Calibration Equation for pH
const float SLOPE = -0.003273;
const float INTERCEPT = 12.706;

// Moisture Calibration Constants
const int DRY_ADC = 4095;   // 0% Moisture
const int WET_ADC = 1500;   // 100% Moisture


void setup() {
  pinMode(25,INPUT_PULLUP);
  Serial.begin(115200);
  SerialBT.begin("Soil_Sathi");
  WiFi.begin();  // no SSID/PWD - get it from the Provisioning APP or from NVS (last successful connection)
  WiFi.onEvent(SysProvEvent);

// BLE Provisioning using the ESP SoftAP Prov works fine for any BLE SoC, including ESP32, ESP32S3 and ESP32C3.
#if CONFIG_BLUEDROID_ENABLED && !defined(USE_SOFT_AP)
  Serial.println("Begin Provisioning using BLE");
  // Sample uuid that user can pass during provisioning using BLE
  uint8_t uuid[16] = {0xb4, 0xdf, 0x5a, 0x1c, 0x3f, 0x6b, 0xf4, 0xbf, 0xea, 0x4a, 0x82, 0x03, 0x04, 0x90, 0x1a, 0x02};
  WiFiProv.beginProvision(
    NETWORK_PROV_SCHEME_BLE, NETWORK_PROV_SCHEME_HANDLER_FREE_BLE, NETWORK_PROV_SECURITY_1, pop, service_name, service_key, uuid, reset_provisioned
  );
  log_d("ble qr");
  WiFiProv.printQR(service_name, pop, "ble");
#else
  Serial.println("Begin Provisioning using Soft AP");
  WiFiProv.beginProvision(NETWORK_PROV_SCHEME_SOFTAP, NETWORK_PROV_SCHEME_HANDLER_NONE, NETWORK_PROV_SECURITY_1, pop, service_name, service_key);
  log_d("wifi qr");
  WiFiProv.printQR(service_name, pop, "softap");
#endif

}

void loop() {
  if (mode == "none") {

    if (WiFi.status() == WL_CONNECTED) {
        mode = "WIFI_MODE";
        Serial.println(">>> WIFI CONNECTED \n STOPPING BLUETOOTH");

        SerialBT.end();
    }

    else if (SerialBT.hasClient()) {
        mode = "BT_MODE";
        Serial.println(">>> BLUETOOTH CONNECTED \n STOPPING WI-FI");

        WiFi.disconnect(true);
    }}
  if(digitalRead(25)== LOW ){
    delay(5000);
    if(digitalRead(25)== LOW ){
      Serial.println("\n reseting wifi credentials...");
      nvs_flash_erase();
      ESP.restart();
    }
  }
  int phADC = readSensor(PH_PIN);
  float pH = calculatePH(phADC);

  int moistureADC = readSensor(MOISTURE_PIN);
  // Calculate stable percentage value
  int moisturePercent = calculateMoisturePercent(moistureADC);

  // Send the stable percentage to Python instead of raw ADC
  sendSensorData(phADC, pH, moisturePercent);

  delay(2000);
}

//====================================================
// Read Sensor with Trimmed Mean Filter
//====================================================
int readSensor(int pin) {
  int samples[NUM_SAMPLES];

  for (int i = 0; i < NUM_SAMPLES; i++) {
    samples[i] = analogRead(pin);
    delay(20);
  }

  // Bubble Sort
  for (int i = 0; i < NUM_SAMPLES - 1; i++) {
    for (int j = 0; j < NUM_SAMPLES - i - 1; j++) {
      if (samples[j] > samples[j + 1]) {
        int temp = samples[j];
        samples[j] = samples[j + 1];
        samples[j + 1] = temp;
      }
    }
  }

  long sum = 0;
  // Ignore lowest 2 and highest 2 values
  for (int i = 2; i < NUM_SAMPLES - 2; i++) {
    sum += samples[i];
  }

  return sum / (NUM_SAMPLES - 4);
}

//====================================================
// Convert ADC to pH
//====================================================
float calculatePH(int adc) {
  return (SLOPE * adc) + INTERCEPT;
}

//====================================================
// Convert ADC to Moisture Percentage
//====================================================
int calculateMoisturePercent(int adc) {
  // Constrain the raw ADC so values outside the calibration limits don't break the percentage calculation
  int constrainedADC = constrain(adc, WET_ADC, DRY_ADC);
  
  // Map the constrained values: 4095 -> 0%, 1500 -> 100%
  int percent = map(constrainedADC, DRY_ADC, WET_ADC, 0, 100);
  
  return percent;
}

//====================================================
// Send Data to Python
//====================================================
void sendSensorData(int adc, float pH, int moisture) {

  String data = "";

  data += "ADC: ";
  data += adc;

  data += " | pH: ";
  data += String(pH, 2);

  data += " | Moisture: ";
  data += moisture;
  data += "%";

  // Always show through USB while we're debugging
  Serial.println(data);

  // Send through whichever wireless connection won
  if (mode == "BT_MODE") {

    SerialBT.println(data);

  }
  else if (mode == "WIFI_MODE") {

     HTTPClient http;

        http.begin(serverURL);
        http.addHeader("Content-Type", "application/json");

        String json = "{";
        json += "\"ph\":" + String(pH, 2) + ",";
        json += "\"moisture\":" + String(moisture) + ",";
        json += "\"adc\":" + String(adc);
        json += "}";

        int responseCode = http.POST(json);

        Serial.print("HTTP response: ");
        Serial.println(responseCode);

        http.end();
  }
}
