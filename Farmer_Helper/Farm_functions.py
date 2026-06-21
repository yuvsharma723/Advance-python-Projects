import math
class crop:
    name = "कोई फसल निर्धारित नहीं की गई है। कृपया सही गणना के लिए फसल चुनें।"
    seed_required_per_acre = 0     # Typical for hybrid sowing
    avg_yield_per_acre = 0           # Good average for a managed farm
    msp = 0                        # 2025-26 Expected MSP
    seed_rate = 0                   # Hybrid seed cost per kg
    miscelaneous_cost_per_acre = 0 # Includes: Land prep (2k), Fertilizer (1.5k), Labor (2k), Misc (1k)
    ph_min = 0
    ph_max = 14

    moisture_min = 0
    moisture_max = 100
    actual_ph= 6.8
    moisture_content= 90 # in percentage , can be fetched by the sensor
    def __init__(self,area):
        if self.name == "कोई फसल निर्धारित नहीं की गई है। कृपया सही गणना के लिए फसल चुनें।":
            self.valid = False
            print("कोई फसल निर्धारित नहीं की गई है। कृपया सही गणना के लिए फसल चुनें।")
            return
        self.valid = True
        self.area_in_acres=float(area)
        
        
        self.seed_required= self.seed_required_per_acre * self.area_in_acres
        self.yield_amount= self.avg_yield_per_acre * self.area_in_acres
        self.revenue= self.msp * self.avg_yield_per_acre * self.area_in_acres
        self.cost= self.seed_rate * self.seed_required_per_acre* self.area_in_acres + self.miscelaneous_cost_per_acre * self.area_in_acres
        self.profit= (self.msp * self.avg_yield_per_acre * self.area_in_acres) - (self.cost)
    def check_soil(self):

        moisture_msg = ""
        ph_msg = ""

        if self.moisture_content < self.moisture_min:
            moisture_msg = "नमी कम है"
        elif self.moisture_min <= self.moisture_content <= self.moisture_max:
            moisture_msg = "नमी उपयुक्त है"
        else:
            moisture_msg = "नमी अधिक है"

        if self.actual_ph < self.ph_min:
            ph_msg = "pH कम है"
        elif self.ph_min <= self.actual_ph <= self.ph_max:
            ph_msg = "pH उपयुक्त है"
        else:
            ph_msg = "pH अधिक है"

        return moisture_msg + " | " + ph_msg
    def calculate_seed_required(self):
        if not self.valid:
            return
        
        return self.seed_required
 
    def calculate_yield(self):
        if not self.valid:
            return
        return self.yield_amount

    def calculate_revenue(self):
        if not self.valid:
            return
        return self.revenue
    
    def calculate_cost(self):
        if not self.valid:
            return
        return self.cost

    def calculate_profit(self):
        if not self.valid:
            return
        return self.profit

class bajra(crop):
    name = "Bajra"
    seed_required_per_acre = 2.5      # Typical for hybrid sowing
    avg_yield_per_acre = 10           # Good average for a managed farm
    msp = 2900                        # 2025-26 Expected MSP
    seed_rate = 250                   # Hybrid seed cost per kg
    miscelaneous_cost_per_acre = 6500 # Includes: Land prep (2k), Fertilizer (1.5k), Labor (2k), Misc (1k)
    ph_min = 6.5
    ph_max = 8.0

    moisture_min = 20
    moisture_max = 55
    def calculate_success_rate(self):

        # Ideal values (center of acceptable range)
        ph_opt = (self.ph_min + self.ph_max) / 2
        moisture_opt = (self.moisture_min + self.moisture_max) / 2

        # Tolerance (how far crop can comfortably handle)
        ph_tolerance = (self.ph_max - self.ph_min) 
        moisture_tolerance = (self.moisture_max - self.moisture_min) 

        # Gaussian scoring
        ph_score = 100 * math.exp(
            -((self.actual_ph - ph_opt) / ph_tolerance*1.5) ** 2
        )

        moisture_score = 100 * math.exp(
            -((self.moisture_content - moisture_opt) / moisture_tolerance*1.5) ** 2
        )

        # Final weighted score
        success_rate = (
            0.65 * ph_score +
            0.35 * moisture_score
        )

        return round(success_rate, 2)
class wheat(crop):
    name = "Wheat"
    seed_required_per_acre = 45
    avg_yield_per_acre = 18
    msp = 2585
    seed_rate = 40
    miscelaneous_cost_per_acre = 8500

    ph_min = 6.0
    ph_max = 7.5

    moisture_min = 40
    moisture_max = 70
    def calculate_success_rate(self):

        # Ideal values (center of acceptable range)
        ph_opt = (self.ph_min + self.ph_max) / 2
        moisture_opt = (self.moisture_min + self.moisture_max) / 2

        # Tolerance (how far crop can comfortably handle)
        ph_tolerance = (self.ph_max - self.ph_min) 
        moisture_tolerance = (self.moisture_max - self.moisture_min) 

        # Gaussian scoring
        ph_score = 100 * math.exp(
            -((self.actual_ph - ph_opt) / ph_tolerance*1.5) ** 2
        )

        moisture_score = 100 * math.exp(
            -((self.moisture_content - moisture_opt) / moisture_tolerance*1.5) ** 2
        )

        # Final weighted score
        success_rate = (
            0.65 * ph_score +
            0.35 * moisture_score
        )

        return round(success_rate, 2)
class mustard(crop):
    name = "Mustard"
    seed_required_per_acre = 2
    avg_yield_per_acre = 8
    msp = 6200
    seed_rate = 700
    miscelaneous_cost_per_acre = 7000

    ph_min = 6.0
    ph_max = 7.3

    moisture_min = 25
    moisture_max = 55
    def calculate_success_rate(self):

        # Ideal values (center of acceptable range)
        ph_opt = (self.ph_min + self.ph_max) / 2
        moisture_opt = (self.moisture_min + self.moisture_max) / 2

        # Tolerance (how far crop can comfortably handle)
        ph_tolerance = (self.ph_max - self.ph_min) 
        moisture_tolerance = (self.moisture_max - self.moisture_min) 

        # Gaussian scoring
        ph_score = 100 * math.exp(
            -((self.actual_ph - ph_opt) / ph_tolerance*1.5) ** 2
        )

        moisture_score = 100 * math.exp(
            -((self.moisture_content - moisture_opt) / moisture_tolerance*1.5) ** 2
        )

        # Final weighted score
        success_rate = (
            0.65 * ph_score +
            0.35 * moisture_score
        )

        return round(success_rate, 2)
class gram(crop):
    name = "Gram"
    seed_required_per_acre = 32
    avg_yield_per_acre = 7
    msp = 5875
    seed_rate = 80
    miscelaneous_cost_per_acre = 6500

    ph_min = 6.0
    ph_max = 7.5

    moisture_min = 35
    moisture_max = 60
    def calculate_success_rate(self):

        # Ideal values (center of acceptable range)
        ph_opt = (self.ph_min + self.ph_max) / 2
        moisture_opt = (self.moisture_min + self.moisture_max) / 2

        # Tolerance (how far crop can comfortably handle)
        ph_tolerance = (self.ph_max - self.ph_min) 
        moisture_tolerance = (self.moisture_max - self.moisture_min) 
        # Gaussian scoring
        ph_score = 100 * math.exp(
            -((self.actual_ph - ph_opt) / ph_tolerance*1.5) ** 2
        )

        moisture_score = 100 * math.exp(
            -((self.moisture_content - moisture_opt) / moisture_tolerance*1.5) ** 2
        )

        # Final weighted score
        success_rate = (
            0.65 * ph_score +
            0.35 * moisture_score
        )

        return round(success_rate, 2)
class rice(crop):
    name = "Rice"
    seed_required_per_acre = 10
    avg_yield_per_acre = 22
    msp = 2441
    seed_rate = 60
    miscelaneous_cost_per_acre = 11000

    ph_min = 5.5
    ph_max = 7.0

    moisture_min = 70
    moisture_max = 100
    def calculate_success_rate(self):

        # Ideal values (center of acceptable range)
        ph_opt = (self.ph_min + self.ph_max) / 2
        moisture_opt = (self.moisture_min + self.moisture_max) /2

        # Tolerance (how far crop can comfortably handle)
        ph_tolerance = (self.ph_max - self.ph_min) 
        moisture_tolerance = (self.moisture_max - self.moisture_min)

        # Gaussian scoring
        ph_score = 100 * math.exp(
            -((self.actual_ph - ph_opt) / ph_tolerance*1.5) ** 2
        )

        moisture_score = 100 * math.exp(
            -((self.moisture_content - moisture_opt) / moisture_tolerance*1.5) ** 2
        )

        # Final weighted score
        success_rate = (
            0.65 * ph_score +
            0.35 * moisture_score
        )

        return round(success_rate, 2)