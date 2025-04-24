import streamlit as st

# 🧱 Class to encapsulate unit conversion logic
class UnitConverter:
    def __init__(self):
        # 📦 Encapsulation: conversion factors are hidden inside class
        self.conversion_factors = {
            "meters_kilometers": 0.001,
            "kilometers_meters": 1000,
            "grams_kilograms": 0.001,
            "kilograms_grams": 1000
        }

    # 🔍 Abstraction: hides internal logic of conversion
    def convert(self, value: float, from_unit: str, to_unit: str) -> str:
        key = f"{from_unit}_{to_unit}"
        if key in self.conversion_factors:
            return value * self.conversion_factors[key]
        else:
            return f"❌ Conversion between {from_unit} and {to_unit} is not possible. Please choose different units."

# 🎯 Streamlit UI logic
def main():
    st.set_page_config(page_title="Unit Converter")
    st.title("Unit Converter (OOP Version)")

    # Create an instance of the converter (🧱 Object created)
    converter = UnitConverter()

    # User Input
    value = st.number_input("Enter the value you want to convert", min_value=1.0, step=1.0)
    from_unit = st.selectbox("From", ["meters", "kilometers", "kilograms", "grams"])
    to_unit = st.selectbox("To", ["meters", "kilometers", "grams", "kilograms"])

    # Convert Button
    if st.button("Convert"):
        result = converter.convert(value, from_unit, to_unit)
        st.write(f"🔁 Result: {result}")

# 🚀 Run the Streamlit app
if __name__ == "__main__":
    main()
