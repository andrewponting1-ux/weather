import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="Swindon Weather", layout="centered")
    st.title("🌤️ Swindon Weather Guide")

    # 2. SETTINGS (Swindon)
    LAT = 51.5558
    LON = -1.7797

    # 3. SECURE API CALL
    try:
        # Pull key from your Streamlit Cloud Secrets
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # Exact 3.0 One Call URL
        url = f"https://api.openweathermap.org{LAT}&lon={LON}&appid={API_KEY}&units=metric"
        
        # Headers to prevent the "Network Block"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            # 3.0 Data structure: current -> temp
            temp = data["current"]["temp"]
            # 3.0 Data structure: current -> weather list -> first item -> description
            desc = data["current"]["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in Swindon")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            st.success("✅ Connection Successful!")
            st.balloons()
            
        elif response.status_code == 401:
            st.warning("⏳ Key not active yet. OpenWeather is still syncing your 3.0 subscription.")
        else:
            st.error(f"❌ Server Error {response.status_code}. Check your OpenWeather subscription.")

    except Exception:
        # SECURE: Hidden error to protect your key from logs
        st.error("📡 Connection still blocked. Try a 'Reboot' from the Streamlit dashboard.")

    if st.button("🔄 Refresh"):
        st.rerun()
