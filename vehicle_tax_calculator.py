class VehicleTaxCalculator:
    def __init__(self):
        self.registration_date = None
        self.vehicle_class = None
        self.drive_type = None
        self.power_kw = None
        self.weight_kg = None
        self.co2_emissions = None
        self.displacement_cc = None

    def calculate_tax_class_L(self):
        """Calculate tax for L1e, L2e, L3e, L4e and L5e vehicles"""
        if self.drive_type == "electric":
            # Electric vehicles
            adjusted_power = max(self.power_kw - 5, 4)
            return round(0.50 * adjusted_power, 2)
        else:
            # Combustion engine vehicles
            if self.registration_date < "2020-10-01":
                # Vehicles registered before Oct 1, 2020
                return round(0.025 * self.displacement_cc, 2)
            else:
                # Vehicles registered after Sept 30, 2020
                adjusted_displacement = max(self.displacement_cc - 52, 0)
                adjusted_co2 = max(self.co2_emissions - 52, 10)
                return round((0.014 * adjusted_displacement) + (0.20 * adjusted_co2), 2)

    def calculate_tax_class_M1(self):
        """Calculate tax for M1 vehicles up to 3.5 tons"""
        if self.drive_type == "electric":
            # Electric vehicles
            # Power component
            adjusted_power = max(self.power_kw - 45, 10)
            power_tax = 0
            
            if adjusted_power <= 35:
                power_tax = adjusted_power * 0.25
            elif adjusted_power <= 60:
                power_tax = (35 * 0.25) + ((adjusted_power - 35) * 0.35)
            else:
                power_tax = (35 * 0.25) + (25 * 0.35) + ((adjusted_power - 60) * 0.45)

            # Weight component
            adjusted_weight = max(self.weight_kg - 900, 200)
            weight_tax = 0
            
            if adjusted_weight <= 500:
                weight_tax = adjusted_weight * 0.015
            elif adjusted_weight <= 1200:
                weight_tax = (500 * 0.015) + ((adjusted_weight - 500) * 0.030)
            else:
                weight_tax = (500 * 0.015) + (700 * 0.030) + ((adjusted_weight - 1200) * 0.045)

            return round(power_tax + weight_tax, 2)
        else:
            # Combustion engine vehicles
            if self.registration_date < "2020-10-01":
                adjusted_power = max(self.power_kw - 24, 0)
                tax = 0
                
                if adjusted_power <= 66:
                    tax = adjusted_power * 0.62
                elif adjusted_power <= 86:
                    tax = (66 * 0.62) + ((adjusted_power - 66) * 0.66)
                else:
                    tax = (66 * 0.62) + (20 * 0.66) + ((adjusted_power - 86) * 0.75)

                return round(max(tax, 6.20), 2)
            else:
                # For vehicles after Sept 30, 2020, calculation depends on hybrid type
                # This is a simplified version for basic combustion engines
                adjusted_power = max(self.power_kw - 24, 0)
                tax = 0
                
                if adjusted_power <= 66:
                    tax = adjusted_power * 0.65
                elif adjusted_power <= 86:
                    tax = (66 * 0.65) + ((adjusted_power - 66) * 0.70)
                else:
                    tax = (66 * 0.65) + (20 * 0.70) + ((adjusted_power - 86) * 0.79)

                return round(max(tax, 6.50), 2)

def main():
    calculator = VehicleTaxCalculator()
    
    print("Austrian Motor Vehicle Insurance Tax Calculator")
    print("---------------------------------------------")
    
    # Get vehicle information
    print("\nVehicle Class:")
    print("1. L-class (motorcycles)")
    print("2. M1-class (passenger cars up to 3.5t)")
    class_choice = input("Select vehicle class (1/2): ")
    
    print("\nDrive Type:")
    print("1. Electric")
    print("2. Combustion/Other")
    drive_choice = input("Select drive type (1/2): ")
    
    registration_date = input("\nRegistration date (YYYY-MM-DD): ")
    
    if drive_choice == "1":
        power = float(input("Electric motor power (kW): "))
        calculator.power_kw = power
        if class_choice == "2":
            weight = float(input("Vehicle weight (kg): "))
            calculator.weight_kg = weight
    else:
        if class_choice == "1":
            displacement = float(input("Engine displacement (cc): "))
            calculator.displacement_cc = displacement
            if registration_date >= "2020-10-01":
                emissions = float(input("CO2 emissions (g/km): "))
                calculator.co2_emissions = emissions
        else:
            power = float(input("Engine power (kW): "))
            calculator.power_kw = power

    calculator.registration_date = registration_date
    calculator.drive_type = "electric" if drive_choice == "1" else "combustion"
    calculator.vehicle_class = "L" if class_choice == "1" else "M1"

    # Calculate tax
    monthly_tax = (calculator.calculate_tax_class_L() if class_choice == "1" 
                  else calculator.calculate_tax_class_M1())

    print(f"\nMonthly insurance tax: €{monthly_tax:.2f}")
    print(f"Annual insurance tax: €{monthly_tax * 12:.2f}")

if __name__ == "__main__":
    main()