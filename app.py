import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. PAGE SETUP
with streamlit_analytics.track():
    st.set_page_config(page_title="Commute Optimizer", layout="centered")
    st.title("🌤️ My Local Weather Guide")

    # 2. LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426},
        "Swindon": {"lat": 51.5558, "lon": -1.7797}
    }

    selected_city = st.selectbox("📍 Select Location:", list(CITIES.keys()))
    lat = CITIES[selected_city]["lat"]
    lon = CITIES[selected_city]["lon"]

    # 3. SECURE API CALL
    try:
        # Pull key from Streamlit Secrets
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # Exact One Call 3.0 URL format with metric units
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        # 10-second timeout to prevent the app from hanging
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            temp = current["temp"]
            desc = current["weather"][0]["description"]
            
            # Display Weather
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            
            if temp < 10:
                st.info("🧥 Chilly out! Wear a coat for your commute.")
            else:
                st.success("✅ Weather looks good for travel!")
        
        elif response.status_code == 401:
            st.error("⚠️ API Key Error: Check your Secrets or wait for activation.")
        elif response.status_code == 402:
            st.error("⚠️ Subscription Error: One Call 3.0 requires a 'Pay-as-you-go' plan (even for the free tier).")
        else:
            st.error(f"⚠️ Server returned error: {response.status_code}")

    except Exception:
        # SECURE: This prevents the app from showing your API key in an error log
        st.error("📡 Connection Error: The app cannot reach the weather server right now.")
