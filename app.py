import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="Swindon Weather", layout="centered")
    st.title("🌤️ Swindon Weather Guide")

    # 2. SETTINGS
    LAT = 51.5558
    LON = -1.7797
    PART = "minutely,hourly,daily,alerts" # Exclude what you don't need

    try:
        # Pull key from your Streamlit Cloud Secrets
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # FIXED: Added 'f' before the string to inject variables and units=metric for Celsius
        #url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude={PART}&appid={API_KEY}&units=metric"
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}&units=metric"
                       
        
        headers = {'User-Agent': 'WeatherApp/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["current"]["temp"]
            desc = data["current"]["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in Swindon")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            st.success("✅ Connection Successful!")
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
