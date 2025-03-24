import streamlit as st
from datetime import datetime
from vehicle_tax_calculator import VehicleTaxCalculator

def main():
    st.set_page_config(
        page_title="Austian Motor Vehicle Insurance Tax Calculator",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.linkedin.com/in/doyouknowmarc/',
            'About': "Entwickelt basierend auf dem [Beschluss des Nationalrates](https://www.parlament.gv.at/dokument/XXVIII/BNR/14/fnameorig_1671984.html). This calculator was developed by [Marc](https://www.linkedin.com/in/doyouknowmarc/) with the help of AI."
            }
    )

    st.title("Austrian Motor Vehicle Insurance Tax Calculator")
    st.write("Calculate your monthly and annual motor vehicle insurance tax based on Austrian regulations.")
   
    # Create sidebar for inputs
    with st.sidebar:
        st.header("Vehicle Information")
        
        # Vehicle class selection - changed default to M1-class
        vehicle_class = st.radio(
            "Vehicle Class",
            ["M1-class (passenger cars up to 3.5t)", "L-class (motorcycles)"]
        )
        
        # Drive type selection
        drive_type = st.radio(
            "Drive Type",
            ["Electric", "Combustion/Other"]
        )
        
        # Registration date
        reg_date = st.date_input(
            "Registration Date",
            datetime.now()
        )
        
        # Vehicle specific inputs based on selections
        if drive_type == "Electric":
            power_kw = st.number_input("Electric Motor Power (kW)", min_value=0.0, value=50.0, step=1.0)
            
            # Weight only needed for M1 electric vehicles
            if vehicle_class == "M1-class (passenger cars up to 3.5t)":
                weight_kg = st.number_input("Vehicle Weight (kg)", min_value=0.0, value=1500.0, step=100.0)
            else:
                weight_kg = 0
                
            displacement_cc = 0
            co2_emissions = 0
        else:
            if vehicle_class == "L-class (motorcycles)":
                displacement_cc = st.number_input("Engine Displacement (cc)", min_value=0.0, value=500.0, step=50.0)
                
                # CO2 emissions only needed for newer motorcycles
                if reg_date >= datetime(2020, 10, 1):
                    co2_emissions = st.number_input("CO2 Emissions (g/km)", min_value=0.0, value=90.0, step=5.0)
                else:
                    co2_emissions = 0
                    
                power_kw = 0
                weight_kg = 0
            else:
                power_kw = st.number_input("Engine Power (kW)", min_value=0.0, value=100.0, step=5.0)
                displacement_cc = 0
                co2_emissions = 0
                weight_kg = 0
    with st.sidebar.container():
        st.divider()
        st.image("Marc.png", use_container_width="never", width=100)
        st.header("Greetings 👋")
        st.write("My name is Marc and I'm trying to earn my very first dollar online through creating helpful tools.")
        st.write("Will you [help](https://ko-fi.com/doyouknowmarc) me? 🙈")
        st.write("Calculation based on: [Budgetsanierungsmaßnahmengesetz 2025 – BSMG 2025 (14/BNR)](https://www.parlament.gv.at/dokument/XXVIII/BNR/14/fnameorig_1671984.html)")
    
    # Calculate tax
    calculator = VehicleTaxCalculator()
    calculator.registration_date = reg_date.strftime("%Y-%m-%d")
    calculator.drive_type = "electric" if drive_type == "Electric" else "combustion"
    calculator.vehicle_class = "L" if vehicle_class == "L-class (motorcycles)" else "M1"
    calculator.power_kw = power_kw
    calculator.weight_kg = weight_kg
    calculator.co2_emissions = co2_emissions
    calculator.displacement_cc = displacement_cc
    
    if calculator.vehicle_class == "L":
        monthly_tax = calculator.calculate_tax_class_L()
    else:
        monthly_tax = calculator.calculate_tax_class_M1()
    
    annual_tax = monthly_tax * 12
    
    # Display results
    st.header("Tax Calculation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Monthly Tax", f"€{monthly_tax:.2f}")
        
    with col2:
        st.metric("Annual Tax", f"€{annual_tax:.2f}")
    
    # Display calculation details
    st.subheader("Calculation Details")
    
    details = {
        "Vehicle Class": vehicle_class,
        "Drive Type": drive_type,
        "Registration Date": reg_date.strftime("%Y-%m-%d")
    }
    
    if power_kw > 0:
        details["Power (kW)"] = f"{power_kw:.1f}"
    
    if weight_kg > 0:
        details["Weight (kg)"] = f"{weight_kg:.1f}"
    
    if displacement_cc > 0:
        details["Engine Displacement (cc)"] = f"{displacement_cc:.1f}"
    
    if co2_emissions > 0:
        details["CO2 Emissions (g/km)"] = f"{co2_emissions:.1f}"
    
    st.json(details)
    
    # Add explanation of calculation
    with st.expander("How is the tax calculated?"):
        st.write("""
        The motor vehicle insurance tax in Austria is calculated based on:
        
        - Vehicle class (L-class for motorcycles, M1-class for passenger cars)
        - Drive type (electric or combustion engine)
        - Registration date (before or after October 1, 2020)
        - Vehicle specifications (power, weight, displacement, CO2 emissions)
        
        The specific formulas are defined in the [Budgetsanierungsmaßnahmengesetz 2025 – BSMG 2025 (14/BNR)](https://www.parlament.gv.at/dokument/XXVIII/BNR/14/fnameorig_1671984.html).
        """)

if __name__ == "__main__":
    main()