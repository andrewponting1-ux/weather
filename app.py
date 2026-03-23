import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING
with streamlit_analytics.track():
    st.title("🌤️ My Local Weather Guide") 
    st.markdown("Powered by BrightSky Weather Service")

    # 2. LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 3. FETCH DATA FROM BRIGHTSKY
    try:
        # We ask for the most recent weather record
        url = f"https://api.brightsky.dev{lat}&lon={lon}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # BrightSky puts the data inside a 'weather' object
            data = response.json()["weather"]
            
            temp = data["temperature"]
            wind = data["wind_speed"]
            condition = data["condition"]
            
            st.header(f"Current Temp: {temp}°C")
            st.write(f"💨 Wind: {wind} km/h")
            st.write(f"☁️ Condition: {condition.capitalize()}")
            
            # Simple Advice
            if temp < 10:
                st.info(f"🧥 It's chilly in {selected_city}. Wrap up warm!")
            elif condition == 'rain':
                st.warning(f"☔ Rain detected in {selected_city}. Take an umbrella!")
            else:
                st.success(f"✅ Looking good in {selected_city}!")
        else:
            st.error(f"Weather service returned error code: {response.status_code}")

    except Exception as e:
        st.error("⚠️ Connection failed. Please try refreshing the page.")
