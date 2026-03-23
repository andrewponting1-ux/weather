import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics
from datetime import datetime

with streamlit_analytics.track():
    st.title("🌤️ My Local Weather Guide")

    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 1. MATCHING THE DEMO URL FORMAT
    # BrightSky uses YYYY-MM-DD for the date parameter
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.brightsky.dev{lat}&lon={lon}&date={today}"

    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            # 2. SELECTING THE FIRST RECORD
            # This endpoint returns a list under the 'weather' key
            weather_list = response.json().get("weather", [])
            
            if weather_list:
                current_data = weather_list[0] # Grab the first (earliest) record for today
                
                temp = current_data["temperature"]
                wind = current_data["wind_speed"]
                condition = current_data["condition"]
                
                st.header(f"{temp}°C in {selected_city}")
                st.write(f"💨 Wind: {wind} km/h")
                st.write(f"☁️ Condition: {condition.capitalize()}")
                
                # Dynamic advice
                if temp < 10:
                    st.info(f"🧥 Chilly in {selected_city}. Dress warmly!")
                else:
                    st.success(f"✅ Enjoy the day in {selected_city}!")
            else:
                st.warning("No weather records found for this location.")
        else:
            st.error(f"Server Error {response.status_code}. Try again in a minute.")

    except Exception as e:
        st.error("⚠️ Connection failed. The weather server might be blocking the cloud.")
