from Farm_functions import *
from flask import Flask, render_template, request
import serial
import time

PORT = "COM7"
BAUD = 115200

def connect_sensor():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)
        return ser, "✅ Sensor Connected"

    except serial.SerialException as e:
        print(e)
        return None, "❌ Sensor Not Connected"
ser, sensor_update = connect_sensor()
def read_sensor():

    if ser is None:
        return None, None

    values_ph = []
    values_moisture = []
    attempts = 0

    while len(values_ph) < 10 and attempts < 30:
        attempts += 1

        line = ser.readline().decode(errors="ignore").strip()

        if not line:
            continue

        try:
            adc, ph, moisture = line.split(",")
            values_ph.append(float(ph))
            values_moisture.append(float(moisture))
        except ValueError:
            continue

    if len(values_ph) == 0:
        return None, None
app = Flask(__name__)

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
            ph, moisture = read_sensor()

            if ph is None:
                return render_template(
                    "index.html",
                    sensor_update="❌ Sensor Not Connected",
                    sensor_ph="--",
                    sensor_moisture="--"
                )
            crop.actual_ph, crop.moisture_content = ph, moisture
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
        return render_template("index.html",sensor_update=sensor_update,sensor_ph=crop.actual_ph,sensor_moisture=crop.moisture_content, suggestion=suggestion, success_rate=success_rate_str, best_crop=best_crop_name, check_soil=check_soil, seed_required=seed_required, expected_yield=expected_yield, revenue=revenue, cost=cost, profit=profit)
    return render_template(
    "index.html",
    sensor_update=sensor_update,
    sensor_ph="--",
    sensor_moisture="--")
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)