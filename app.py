import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE SETUP
with streamlit_analytics.track():
    st.set_page_config(page_title="My Local Weather", layout="centered")
    
    # You can change these titles to whatever you want!
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

    # 3. GET WEATHER (The main part)
    try:
        w_url = f"https://api.open-meteo.com{lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(w_url, timeout=5) # Added a 5-second timeout
        weather_data = w_res.json()
        
        temp = weather_data["current_weather"]["temperature"]
        wind = weather_data["current_weather"]["windspeed"]

        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{temp}°C")
        col2.metric("Wind Speed", f"{wind} km/h")
        
    except Exception:
        st.error("⚠️ Could not load weather. Check your connection.")

    # 4. GET AIR QUALITY (The extra part - keeps app running even if this fails)
    try:
        a_url = f"https://air-quality-api.open-meteo.com{lat}&longitude={lon}&current=european_aqi"
        a_res = requests.get(a_url, timeout=5)
        air_data = a_res.json()
        
        aqi = air_data["current"]["european_aqi"]
        st.info(f"Air Quality Index (AQI): {aqi}")
    except Exception:
        st.warning("💨 Air Quality data currently unavailable.")

    # 5. MAP
    st.subheader(f"Location Map: {selected_city}")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon]).add_to(m)
    st_folium(m, height=300, width=700)
