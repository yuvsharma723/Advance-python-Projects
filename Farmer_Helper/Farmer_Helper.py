from Farm_functions import *
from flask import Flask, render_template, request

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

        area = float(request.form["area"])
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
    return render_template("index.html", suggestion=suggestion,success_rate=success_rate_str, best_crop=best_crop_name, check_soil=check_soil, seed_required=seed_required, expected_yield=expected_yield, revenue=revenue, cost=cost, profit=profit)
if __name__ == "__main__":
    app.run(debug=True)