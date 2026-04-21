import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import matplotlib.pyplot as plt
import calendar

# Load model
pipeline = joblib.load("aqi_pipeline.pkl")

st.set_page_config(page_title="AQI Predictor", layout="wide")

st.title("===AQI Prediction==== ")

# --- SIDEBAR ---
st.sidebar.header("📍Locations and weather condition")

location = st.sidebar.selectbox(
    "Location",
    ["Connaught Place", "Dwarka", "IGI Airport", "Okhla Phase III", "Rohini"]
)

condition = st.sidebar.selectbox(
    "Weather Condition",
    [
        "Drizzle: Dense",
        "Drizzle: Light",
        "Drizzle: Moderate",
        "Fog",
        "Mainly clear",
        "Overcast",
        "Partly cloudy",
        "Rain: Heavy",
        "Rain: Moderate",
        "Rain: Slight"
    ]
)

# Auto time
current_hour = datetime.now().hour
current_month = datetime.now().month

# --- MAIN INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Weather")
    temp = st.number_input("Temperature (°C)", value=25.0, step=1.0)
    humidity = st.slider("Humidity (%)", 0, 100, 50)
    pressure = st.number_input("Pressure (mb)", value=1010.0, step=1.0)
    wind = st.number_input("Wind Speed (kph)", value=10.0, step=1.0)

with col2:
    st.subheader("💨 Pollution")
    pm25 = st.number_input("PM2.5", value=100.0, step=1.0)
    pm10 = st.number_input("PM10", value=150.0, step=1.0)
    co = st.number_input("CO", value=1.0, step=1.0)
    no2 = st.number_input("NO2", value=40.0, step=1.0)

st.markdown("---")

# --- PREDICTION ---
if st.button("🚀 Predict AQI"):

    input_data = pd.DataFrame([{
        "location": location,
        "condition_text": condition,
        "temp_c": temp,
        "humidity": humidity,
        "pressure_mb": pressure,
        "windspeed_kph": wind,
        "pm2_5": pm25,
        "pm10": pm10,
        "co": co,
        "no2": no2,
        "hour": current_hour,
        "month": current_month
    }])

    prediction = pipeline.predict(input_data)[0]

    # --- RESULT DISPLAY ---
    st.markdown("## 🌫️ AQI Result")

    st.write(f"📍 Location: **{location}**")
    st.write(f"🌤️ Condition: **{condition}**")
    time_display = datetime.now().strftime("%I:%M %p")
    st.write(f"🕒 Time: **{time_display}**")
    month_name = calendar.month_name[current_month]
    st.write(f"📅 Month: **{month_name}**")

    # AQI Categorymonth_name = calendar.month_name[current_month]
    if prediction <= 50:
        st.success(f"AQI: {prediction:.2f} (Good 😊)")
    elif prediction <= 100:
        st.info(f"AQI: {prediction:.2f} (Moderate 🙂)")
    elif prediction <= 200:
        st.warning(f"AQI: {prediction:.2f} (Poor 😷)")
    else:
        st.error(f"AQI: {prediction:.2f} (Hazardous ☠️)")

    

    # --- SIMPLE VISUALIZATION ---
    st.markdown("## 📊 Pollution Overview")

    features = ["PM2.5", "PM10", "CO", "NO2"]
    values = [pm25, pm10, co, no2]

    chart_data = pd.DataFrame({
      "Pollutant": features,
      "Value": values
      }).set_index("Pollutant")

    st.bar_chart(chart_data)


