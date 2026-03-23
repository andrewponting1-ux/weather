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

    # 3. API CALL
    try:
        # Pulling your NEW key from Secrets
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # EXACT URL FORMAT
        url = f"https://api.openweathermap.org{coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            # Weather description is a list, so we grab the first item
            desc = data["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            
            if temp < 10:
                st.info("🧥 Chilly out there! Dress warmly.")
            else:
                st.success("✅ Weather looks good!")
        else:
            # Simple error if the API key isn't active yet
            st.error("⚠️ Server error. Your new key might need an hour to activate.")

    except Exception:
        # This keeps your key hidden if the connection fails
        st.error("⚠️ Connection failed. Please try refreshing in a moment.")
