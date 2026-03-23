import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING: Using the patched analytics library
with streamlit_analytics.track():
    
    st.set_page_config(page_title="🚲 SHIFT: Commute Optimizer", layout="centered")

    st.title("🚲 SHIFT: Commute Optimizer")
    st.markdown("Weather • Air Quality • Pollen • Travel Advice")

    # 2. HARDCODED LOCATIONS: Add as many as you like here
    CITIES = {
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426},
        "Birmingham": {"lat": 52.4862, "lon": -1.8904},
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "Glasgow": {"lat": 55.8642, "lon": -4.2518}
    }

    # 3. USER SELECTION
    selected_city = st.selectbox("📍 Select your location:", list(CITIES.keys()))
    coords = CITIES[selected_city]
    lat, lon = coords["lat"], coords["lon"]

    # 4. WEATHER DATA: Calling Open-Meteo
    # We fetch current weather, air quality, and pollen in one go
    WEATHER_URL = "https://api.open-meteo.com"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "hourly": "pm10,pm2_5,pollen_graph_birch,pollen_graph_grass",
        "timezone": "auto"
    }

    try:
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        # Display Current Weather
        current = data["current"]
        temp = current["temperature_2m"]
        wind = current["wind_speed_10m"]
        
        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{temp}°C")
        col2.metric("Wind Speed", f"{wind} km/h")

        # 5. MAP VIEW: Show the selected location
        st.subheader(f"Map: {selected_city}")
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=selected_city).add_to(m)
        st_folium(m, height=300, width=700)

        # 6. TRAVEL ADVICE: Simple logic based on weather
        st.subheader("🚲 Commute Advice")
        if temp < 5:
            st.info("❄️ It's cold! Wear thermal layers for your ride.")
        elif wind > 25:
            st.warning("💨 High winds! Be careful on open roads.")
        else:
            st.success("✅ Weather looks good for a cycle today!")

    except Exception as e:
        st.error("Wait! We couldn't fetch the weather data right now. Please try again in a moment.")
