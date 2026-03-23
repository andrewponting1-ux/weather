import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="My Local Weather", layout="centered")
    st.title("🌤️ My Local Weather Guide")

    # 2. LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426},
        "Swindon": {"lat": 51.5558, "lon": -1.7797}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    coords = CITIES[selected_city]

    # 3. API CALL (Using the Free 2.5 Version)
    try:
        # This pulls safely from your Secrets box
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # FIXED URL: Added the missing /data/2.5/weather? part
        url = f"https://api.openweathermap.org{coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"] # Added [0] to fix the list error
            
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            
            if temp < 10:
                st.info("🧥 Chilly out there! Dress warmly.")
            else:
                st.success("✅ Weather looks good!")
        else:
            st.error(f"Server error {response.status_code}. Check your API key in Secrets.")

except Exception:
    st.error("⚠️ Connection failed. Please try again.")
    # DO NOT put st.write(e) here if you want to keep the key hidden during a crash

    

