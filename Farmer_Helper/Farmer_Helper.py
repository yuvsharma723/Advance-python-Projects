class crop:
    name = "no crop is specified(hence everything is zero)"
    seed_required_per_acre = 0     # Typical for hybrid sowing
    avg_yield_per_acre = 0           # Good average for a managed farm
    msp = 0                        # 2025-26 Expected MSP
    seed_rate = 0                   # Hybrid seed cost per kg
    miscelaneous_cost_per_acre = 0 # Includes: Land prep (2k), Fertilizer (1.5k), Labor (2k), Misc (1k)
    def __init__(self):
        self.moisture_content= 75 # in percentage , can be fetched by the sensor
        if self.name == "no crop is specified(hence everything is zero)":
            self.valid = False
            print("No crop specified. Please specify a crop to get accurate calculations.")
            return
        self.valid = True
        while True:
            try:
                self.area_in_acres=float(input(f"enter the area in acres for {self.name}: "))
                break
            except ValueError :
                print("Invalid input. Please enter a valid number.")
        
        
        self.seed_required= self.seed_required_per_acre * self.area_in_acres
        self.yield_amount= self.avg_yield_per_acre * self.area_in_acres
        self.revenue= self.msp * self.avg_yield_per_acre * self.area_in_acres
        self.cost= self.seed_rate * self.seed_required_per_acre* self.area_in_acres + self.miscelaneous_cost_per_acre * self.area_in_acres
        self.profit= (self.msp * self.avg_yield_per_acre * self.area_in_acres) - (self.cost)
    def calculate_seed_required(self):
        if not self.valid:
            return
        
        print(f"seed required for crop {self.name} in {self.area_in_acres} acres is {self.seed_required} kg")

    def calculate_yield(self):
        if not self.valid:
            return
        print(f"expected yield for crop {self.name} in {self.area_in_acres} acres is {self.yield_amount} quintals")

    def calculate_revenue(self):
        if not self.valid:
            return
        print(f"expected revenue for crop {self.name} in {self.area_in_acres} acres is {self.revenue} rs")
    
    def calculate_cost(self):
        if not self.valid:
            return
        print(f"estimated cost for crop {self.name} in {self.area_in_acres} acres is {self.cost} rs")

    def calculate_profit(self):
        if not self.valid:
            return
        print(f"estimated profit for crop {self.name} in {self.area_in_acres} acres is {self.profit} rs")
    
class bajra(crop):
    name = "Bajra"
    seed_required_per_acre = 2.5      # Typical for hybrid sowing
    avg_yield_per_acre = 10           # Good average for a managed farm
    msp = 2775                        # 2025-26 Expected MSP
    seed_rate = 250                   # Hybrid seed cost per kg
    miscelaneous_cost_per_acre = 6500 # Includes: Land prep (2k), Fertilizer (1.5k), Labor (2k), Misc (1k)
bajra_farm= bajra()
if bajra_farm.moisture_content < 60:
    print("soil is dry, irrigation is needed")
elif 60<= bajra_farm.moisture_content <= 80:
    print("soil moisture is optimal for growth")
else:
    print("soil is too wet, drainage is needed")
bajra_farm.calculate_seed_required()
bajra_farm.calculate_yield()
bajra_farm.calculate_revenue()
bajra_farm.calculate_cost()
bajra_farm.calculate_profit()
c = crop()
c.calculate_seed_required()
c.calculate_yield()
c.calculate_revenue()
b= bajra()
b.calculate_seed_required()
b.calculate_yield()