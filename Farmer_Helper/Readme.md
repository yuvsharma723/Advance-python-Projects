# 🌾 Farmer Helper (किसान मित्र)

A Flask-based Smart Agriculture application that analyzes **soil pH**,
**soil moisture**, and **farm area** to recommend the most suitable crop
while estimating seed requirement, expected yield, revenue, cost, and
profit.

The system supports both **manual data entry** and **real-time ESP32
sensor integration**, making it suitable for educational demonstrations
and smart farming applications.

------------------------------------------------------------------------

## 👨‍💻 Author

**Yuv Sharma**

GitHub: **[@yuvsharma723](https://github.com/yuvsharma723)**

------------------------------------------------------------------------

# ✨ Features

## 🌱 Smart Crop Recommendation

The application analyzes soil conditions and recommends the most
suitable crop based on:

-   Soil pH
-   Soil Moisture
-   Farm Area

Currently supported crops:

-   🌾 Bajra
-   🌾 Wheat
-   🌾 Rice
-   🌼 Mustard
-   🌱 Gram

## 📊 Agricultural Calculations

For the recommended crop, the application calculates:

-   🌱 Seed Requirement
-   🌾 Expected Yield
-   💰 Estimated Revenue
-   💸 Estimated Cost
-   📈 Estimated Profit
-   📊 Success Rate

## 🔬 Soil Analysis

The application evaluates:

-   Soil pH
-   Soil Moisture
-   Soil Suitability
-   Irrigation/Drainage Suggestions

## 🌐 Web Interface

Built using **Flask**, the web interface allows users to:

-   Enter values manually
-   Read live sensor data from ESP32
-   View recommendations instantly
-   Display soil information clearly

## 🤖 ESP32 Sensor Integration

Connected Sensors:

-   pH Sensor
-   Capacitive Soil Moisture Sensor

Sensor values are filtered, averaged, processed, and displayed on the
web application.

------------------------------------------------------------------------

# 🛠 Technologies Used

-   Python
-   Arduino C++
-   Flask
-   HTML
-   CSS
-   ESP32

------------------------------------------------------------------------

# 📁 Project Structure

``` text
Farmer_Helper/
│
├── Farmer_Helper.py
├── Farm_functions.py
├── requirements.txt
│
├── Arduino/
│   └── SmartSoilAnalyzer.ino
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── README.md
```

------------------------------------------------------------------------

# ⚙️ How It Works

1.  User enters farm area.
2.  Select **Manual Mode** or **Sensor Mode**.
3.  The application receives soil pH and moisture values.
4.  Soil conditions are evaluated.
5.  Success rate is calculated for every crop.
6.  The best crop is recommended.
7.  The application displays:
    -   Recommended Crop
    -   Success Rate
    -   Soil Analysis
    -   Seed Requirement
    -   Expected Yield
    -   Revenue
    -   Cost
    -   Profit

------------------------------------------------------------------------

# 🚀 Installation

Clone the repository

``` bash
git clone https://github.com/yuvsharma723/Farmer_Helper.git
```

Install dependencies

``` bash
pip install -r requirements.txt
```

Upload the Arduino sketch to the ESP32.

Update the COM port inside `Farmer_Helper.py`.

Run:

``` bash
python Farmer_Helper.py
```

Open:

    http://127.0.0.1:5000

------------------------------------------------------------------------

# 🔌 Serial Communication

ESP32 sends data in the format:

``` text
ADC,pH,Moisture
```

Example:

``` text
1187,8.74,64
```

------------------------------------------------------------------------

# 🌱 Future Improvements

-   Live sensor dashboard
-   Real-time graphs
-   Weather API integration
-   GPS-based soil mapping
-   Cloud database support
-   Live market prices
-   Mobile application
-   AI-based crop recommendation

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

------------------------------------------------------------------------

# 📜 License

This project is intended for educational and research purposes.

------------------------------------------------------------------------

# ⭐ About the Project

**Farmer Helper** combines **ESP32**, **sensor technology**, and
**Python Flask** to demonstrate how IoT can help farmers make informed
agricultural decisions through real-time soil analysis and crop
recommendation.
