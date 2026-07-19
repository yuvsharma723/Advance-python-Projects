/*
====================================================
   Inspire Project - Smart Soil Analyzer
   Board : ESP32
====================================================
*/

const int PH_PIN = 34;
const int MOISTURE_PIN = 4;

const int NUM_SAMPLES = 20;

// Calibration Equation for pH
const float SLOPE = -0.003273;
const float INTERCEPT = 12.706;

// Moisture Calibration Constants
const int DRY_ADC = 4095;   // 0% Moisture
const int WET_ADC = 1500;   // 100% Moisture

void setup() {
  Serial.begin(115200);
}

void loop() {
  int phADC = readSensor(PH_PIN);
  float pH = calculatePH(phADC);

  int moistureADC = readSensor(MOISTURE_PIN);
  // Calculate stable percentage value
  int moisturePercent = calculateMoisturePercent(moistureADC);

  // Send the stable percentage to Python instead of raw ADC
  sendToPython(phADC, pH, moisturePercent);

  delay(1000);
}

//====================================================
// Read Sensor with Trimmed Mean Filter
//====================================================
int readSensor(int pin) {
  int samples[NUM_SAMPLES];

  for (int i = 0; i < NUM_SAMPLES; i++) {
    samples[i] = analogRead(pin);
    delay(10);
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
void sendToPython(int adc, float pH, int moisture) {
  Serial.print(adc);
  Serial.print(",");

  Serial.print(pH, 2);
  Serial.print(",");
  
  Serial.println(moisture); // This now sends the stable 0-100% value
}

