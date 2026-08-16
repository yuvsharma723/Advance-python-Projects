from Farm_functions import *
from flask import Flask, render_template, request
from datetime import datetime
from zoneinfo import ZoneInfo
import time

app = Flask(__name__)
latest_sensor = {
    "ph": None,
    "moisture": None,
    "adc": None
}
sensor_history = []
last_sensor_time = None

@app.route("/sensor", methods=["POST", "GET"])
def receive_sensor():

    if request.method == "POST":
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "No data received"}, 400

        latest_sensor["ph"] = data.get("ph")
        latest_sensor["moisture"] = data.get("moisture")
        latest_sensor["adc"] = data.get("adc")
        global last_sensor_time
        last_sensor_time = time.time()
        sensor_history.append({
            "time": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S"),
            "ph": latest_sensor["ph"],
            "moisture": latest_sensor["moisture"]
        })

        if len(sensor_history) > 100:
            sensor_history.pop(0)

        print("📡 Received from ESP32:", latest_sensor)

        return {"status": "received"}, 200

    return {**latest_sensor,
            "status": sensor_status()}
@app.route("/sensor-history")
def sensor_history_data():
    return sensor_history
def sensor_status():

    if last_sensor_time is None:
        return "❌ Sensor Not Connected"

    if time.time() - last_sensor_time > 20:
        return "❌ Sensor Not Connected"
    if latest_sensor["ph"] is None or latest_sensor["moisture"] is None:
        return "❌ Sensor Not Connected"
    return "✅ Sensor Connected"
@app.route("/", methods=["GET", "POST"])
def home():
    suggestion = ""
    success_rate_str = ""
    check_soil = ""
    seed_required = ""
    expected_yield = ""
    revenue = ""
    cost = ""
    profit = ""
    best_crop_name = ""
    crop_suitable_for_soil = ""
   

    if request.method == "POST":

        mode = request.form.get("mode")
        if mode == "manual":
            crop.actual_ph = float(request.form["ph"])
            crop.moisture_content = float(request.form["moisture"])
        elif mode == "sensor":

            ph = latest_sensor["ph"]
            moisture = latest_sensor["moisture"]
            if sensor_status() != "✅ Sensor Connected":
                return render_template(
                    "index.html",
                    sensor_update="❌ Sensor Not Connected",
                    sensor_ph="--",
                    sensor_moisture="--",
                    suggestion="सेंसर से अभी डेटा प्राप्त नहीं हो रहा है।"
                )


            if ph in (None, "", "None", "--") or moisture in (None, "", "None", "--"):
                return render_template(
                    "index.html",
                    sensor_update="❌ No Wi-Fi sensor data received",
                    sensor_ph="--",
                    sensor_moisture="--"
                )

            crop.actual_ph = ph
            crop.moisture_content = moisture
        area = float(request.form["area"])
        if area <= 0:
            suggestion = "कृपया एक मान्य क्षेत्रफल दर्ज करें।"
            return render_template("index.html", suggestion=suggestion)
        else:
            success_rate_rice = rice(area).calculate_success_rate()
            success_rate_bajra = bajra(area).calculate_success_rate()
            success_rate_wheat = wheat(area).calculate_success_rate()
            success_rate_mustard = mustard(area).calculate_success_rate()
            success_rate_gram = gram(area).calculate_success_rate()
            success_rates = {
                rice: success_rate_rice,
                bajra: success_rate_bajra,
                wheat: success_rate_wheat,
                mustard: success_rate_mustard,
                gram: success_rate_gram
            }
            crop_suitable_for_soil = max(
                success_rates,
                key=success_rates.get
            )
            success_rate_str = str(success_rates[crop_suitable_for_soil]) + "%"
            if success_rates[crop_suitable_for_soil] >= 80:
                suggestion = "इस फसल के लिए मिट्टी अत्यंत उपयुक्त है"
            elif success_rates[crop_suitable_for_soil] >= 70:
                suggestion = "इस फसल के लिए मिट्टी उपयुक्त है"
            elif success_rates[crop_suitable_for_soil] >= 45:
                suggestion = "सीमित सफलता की संभावना है"
            else:
                suggestion = "इस फसल की अनुशंसा नहीं की जाती"
            best_crop = crop_suitable_for_soil(area)
            best_crop_name = best_crop.name
            check_soil=best_crop.check_soil()
            seed_required=best_crop.calculate_seed_required()
            expected_yield=best_crop.calculate_yield()
            revenue=best_crop.calculate_revenue()
            cost=best_crop.calculate_cost()
            profit=best_crop.calculate_profit()
        revenue = f" {revenue:,.0f}"
        cost = f" {cost:,.0f}"
        profit = f" {profit:,.0f}"
        return render_template("index.html",sensor_update=sensor_status(),sensor_ph=crop.actual_ph,sensor_moisture=crop.moisture_content, suggestion=suggestion, success_rate=success_rate_str, best_crop=best_crop_name, check_soil=check_soil, seed_required=seed_required, expected_yield=expected_yield, revenue=revenue, cost=cost, profit=profit,
                # Values needed by "Check Another Crop"
                ph=crop.actual_ph,
                moisture=crop.moisture_content,
                area=area
            )
    return render_template(
    "index.html",
    sensor_update=sensor_status(),
    sensor_ph="--",
    sensor_moisture="--")
@app.route("/check-crop", methods=["POST"])
def check_crop():

    crop_name = request.form.get("crop_name")
    ph = request.form.get("ph")
    moisture = request.form.get("moisture")

    if ph in (None, "", "None", "--") or moisture in (None, "", "None", "--"):
         return render_template(
        "index.html",
        sensor_update="❌ Sensor Not Connected",
        sensor_ph="--",
        sensor_moisture="--",
        suggestion="सेंसर से डेटा उपलब्ध नहीं है।"
         )
    ph = float(request.form.get("ph"))
    moisture = float(request.form.get("moisture"))
    area = float(request.form.get("area"))

    crop_classes = {
        "rice": rice,
        "bajra": bajra,
        "wheat": wheat,
        "mustard": mustard,
        "gram": gram
    }

    selected_class = crop_classes.get(crop_name)

    if selected_class is None:
        return "Invalid crop selected", 400

    selected_crop = selected_class(area)

    selected_crop.actual_ph = ph
    selected_crop.moisture_content = moisture

    success_rate = selected_crop.calculate_success_rate()

    check_soil = selected_crop.check_soil()
    seed_required = selected_crop.calculate_seed_required()
    expected_yield = selected_crop.calculate_yield()
    revenue = selected_crop.calculate_revenue()
    cost = selected_crop.calculate_cost()
    profit = selected_crop.calculate_profit()

    return render_template(
        "index.html",

        sensor_update=sensor_status(),
        sensor_ph=ph,
        sensor_moisture=moisture,

        best_crop=selected_crop.name,
        success_rate=str(success_rate) + "%",

        suggestion="यह आपकी चुनी हुई फसल के लिए मिट्टी की उपयुक्तता है।",

        check_soil=check_soil,
        seed_required=seed_required,
        expected_yield=expected_yield,

        revenue=f" {revenue:,.0f}",
        cost=f" {cost:,.0f}",
        profit=f" {profit:,.0f}",

        ph=ph,
        moisture=moisture,
        area=area
    )
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000, use_reloader=False)