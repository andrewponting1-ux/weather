import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="UK Weather Guide", layout="centered")
    st.title("🌤️ UK Weather Guide")

    # 2. SETTINGS - Locations
    LOCATIONS = {
        "Swindon": {"lat": 51.5558, "lon": -1.7797},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "Oxford": {"lat": 51.7520, "lon": -1.2577}
    }
    
    selected_city = st.selectbox("Select a Location:", list(LOCATIONS.keys()))
    city = LOCATIONS[selected_city]
    
    # We only exclude minutely and alerts to keep the data light but useful
    PART = "minutely,alerts" 

    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # API URL
        url = f"https://api.openweathermap.org{city['lat']}&lon={city['lon']}&exclude={PART}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            
            # --- NEW DATA FIELDS ---
            temp = current["temp"]
            feels_like = current["feels_like"]
            humidity = current["humidity"]
            uv_index = current["uvi"]
            wind_speed = current["wind_speed"]
            desc = current["weather"][0]["description"]
            icon = current["weather"][0]["icon"]

            # --- VISUAL LAYOUT ---
            st.header(f"Current Weather in {selected_city}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.image(f"http://openweathermap.org{icon}@4x.png")
                st.metric("Temp", f"{round(temp, 1)}°C")
            
            with col2:
                st.write("") # Spacer
                st.write("") # Spacer
                st.metric("Feels Like", f"{round(feels_like, 1)}°C")
                st.metric("Humidity", f"{humidity}%")
            
            with col3:
                st.write("") # Spacer
                st.write("") # Spacer
                st.metric("Wind Speed", f"{round(wind_speed, 1)} m/s")
                st.metric("UV Index", uv_index)

            st.subheader(f"☁️ Condition: {desc.capitalize()}")
            st.success("✅ Data Updated")
            
        elif response.status_code == 401:
            st.warning("🔑 API Key issue: Check your One Call 3.0 subscription.")
        else:
            st.error(f"❌ Error {response.status_code}: {response.reason}")

    except Exception as e:
        st.error("📡 Connection error. Check your internet or API subscription.")

    if st.button("🔄 Refresh"):
        st.rerun()
