import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'nutrition_data.csv')

# Load CSV with full path
food_data = pd.read_csv(csv_path)

st.title("🥗 Healthy Plate - Calorie & Nutrition Tracker")

# Rest of your code follows...
food_options = st.multiselect("Select food items", food_data['Food'])
selected = food_data[food_data['Food'].isin(food_options)]

if not selected.empty:
    st.subheader("Enter Quantity (grams)")
    quantities = {}
    for food in selected['Food']:
        quantities[food] = st.number_input(f"{food} (g)", min_value=0, value=100)

    total = {'Calories': 0, 'Protein': 0, 'Fat': 0, 'Carbs': 0}
    for food in selected['Food']:
        row = food_data[food_data['Food'] == food].iloc[0]
        factor = quantities[food] / 100
        total['Calories'] += row['Calories'] * factor
        total['Protein'] += row['Protein'] * factor
        total['Fat'] += row['Fat'] * factor
        total['Carbs'] += row['Carbs'] * factor

    st.success(f"Total Calories: {total['Calories']:.2f} kcal")
    st.write(f"Protein: {total['Protein']:.2f} g")
    st.write(f"Fat: {total['Fat']:.2f} g")
    st.write(f"Carbs: {total['Carbs']:.2f} g")

    fig = px.pie(
        names=['Protein', 'Fat', 'Carbs'],
        values=[total['Protein'], total['Fat'], total['Carbs']],
        title="Macronutrient Distribution"
    )
    st.plotly_chart(fig)
