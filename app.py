import streamlit as st
import openmeteo_sdk
import pandas as pd
from retry_requests import retry
import requests_cache
import streamlit_analytics2 as streamlit_analytics

# 1. SETUP THE SECURE CLIENT
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_sdk.Client(session=retry_session)

with streamlit_analytics.track():
    st.title("🌤️ My Local Weather Guide")

    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 2. FETCH DATA USING THE OFFICIAL SDK
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m"
        }
        # This is the "Safe" way to call Open-Meteo now
        responses = openmeteo.weather_api("https://api.open-meteo.com", params=params)
        response = responses[0]

        # Process results
        current = response.Current()
        temp = current.Variables(0).Value()
        wind = current.Variables(1).Value()

        st.header(f"Current Temp: {round(temp, 1)}°C")
        st.write(f"Wind Speed: {round(wind, 1)} km/h")
        
        if temp < 10:
            st.info(f"🧥 Chilly in {selected_city}!")
        else:
            st.success("😎 Nice weather!")

    except Exception as e:
        st.error("⚠️ The weather service is still blocking the cloud server. Try again in a minute.")
        st.write(f"Debug Info: {e}")
