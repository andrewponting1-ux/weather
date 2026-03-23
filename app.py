import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="UK Weather Guide", layout="centered")
    st.title("🌤️ UK Weather Guide")

    # 2. SETTINGS - This is the part that changes for the dropdown
    locations = {
        "Swindon": [51.5558, -1.7797],
        "London": [51.5074, -0.1278],
        "Bristol": [51.4545, -2.5879]
    }
    
    selected_city = st.selectbox("Select a Location:", list(locations.keys()))
    
    # We assign the coordinates based on your choice
    LAT = locations[selected_city][0]
    LON = locations[selected_city][1]
    
    PART = "minutely,hourly,daily,alerts"

    try:
        # Pull key from your Streamlit Cloud Secrets
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # URL now uses the LAT and LON from the dropdown
        url = f"https://api.openweathermap.org{LAT}&lon={LON}&exclude={PART}&appid={API_KEY}&units=metric"
        
        headers = {'User-Agent': 'WeatherApp/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["current"]["temp"]
            # Added back the [0] index which is required for the description
            desc = data["current"]["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            st.success(f"✅ Connection Successful!")
            st.balloons()
            
        elif response.status_code == 401:
            st.warning("🔑 API Key issue: Ensure your One Call 3.0 subscription is active.")
        else:
            st.error(f"❌ Error {response.status_code}: {response.reason}")

    except KeyError:
        st.error("🔑 Missing Secret: Add 'OPENWEATHER_API_KEY' to your Streamlit Secrets.")
    except Exception as e:
        st.error("📡 Connection error. Check your internet or API limit.")

    if st.button("🔄 Refresh"):
        st.rerun()
