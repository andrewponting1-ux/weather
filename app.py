import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING
with streamlit_analytics.track():
    
    # You can change this title to whatever you want!
    st.set_page_config(page_title="My Weather App", layout="centered")
    st.title("🌤️ My Local Weather Guide") 
    st.markdown("Custom Weather • Air Quality • Advice")

    # 2. YOUR SET LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 3. GET WEATHER & AIR QUALITY
    try:
        # Fetch basic weather
        w_res = requests.get(f"https://api.open-meteo.com{lat}&longitude={lon}&current_weather=true")
        # Fetch air quality (Separate link)
        a_res = requests.get(f"https://air-quality-api.open-meteo.com{lat}&longitude={lon}&current=european_aqi,pm10,pm2_5&hourly=alder_pollen,birch_pollen,grass_pollen")
        
        weather_data = w_res.json()
        air_data = a_res.json()

        # Display Results
        temp = weather_data["current_weather"]["temperature"]
        aqi = air_data["current"]["european_aqi"]

        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{temp}°C")
        col2.metric("Air Quality (AQI)", f"{aqi}")

        # 4. MAP
        st.subheader(f"Map: {selected_city}")
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon]).add_to(m)
        st_folium(m, height=300, width=700)

    except Exception as e:
        st.error("Connection error. Please check your internet or try again later.")

