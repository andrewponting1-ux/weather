import streamlit as st
import requests
from datetime import datetime
import streamlit_analytics2 as streamlit_analytics

# 1. PAGE SETUP
with streamlit_analytics.track():
    st.set_page_config(page_title="Commute Optimizer", layout="centered")
    st.title("🌤️ My Local Weather Guide")
    st.markdown("One Call 3.0 • Secure API Connection")

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
        
        # One Call 3.0 URL
        url = f"https://api.openweathermap.org{lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            temp = current["temp"]
            desc = current["weather"][0]["description"] # Standard formatting for descriptions
            
            # Display Weather
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            
            # Timestamp for the user
            now = datetime.now().strftime("%H:%M")
            st.caption(f"Last updated at {now}")
            
            if temp < 10:
                st.info("🧥 Chilly out! Dress warmly.")
            else:
                st.success("✅ Weather looks good for travel!")
        
        elif response.status_code == 401:
            st.warning("⏳ Your key is not active yet. OpenWeather can take up to 2 hours to activate new subscriptions.")
        else:
            st.error(f"⚠️ Server returned error: {response.status_code}")

    except Exception:
        # SECURE: Hidden error to protect your key
        st.error("📡 Connection Error: The app cannot reach the weather server.")

    if st.button("🔄 Refresh Now"):
        st.rerun()
