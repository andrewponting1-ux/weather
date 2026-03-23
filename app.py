import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="Swindon Weather", layout="centered")
    st.title("🌤️ Swindon Weather Guide")

    # 2. FIXED SETTINGS (Swindon)
    LAT = 51.5558
    LON = -1.7797
    # We exclude what we don't need to keep the response fast
    PART = "minutely,hourly,daily,alerts"

    try:
        # Pull key from your Streamlit Cloud Secrets
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # URL using f-string for coordinates and API key
        url = f"https://api.openweathermap.org{LAT}&lon={LON}&exclude={PART}&appid={API_KEY}&units=metric"
        
        headers = {'User-Agent': 'WeatherApp/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            
            # --- EXTRACTING THE NEW DATA ---
            temp = current["temp"]
            feels_like = current["feels_like"]
            humidity = current["humidity"]
            uv_index = current["uvi"]
            wind_speed = current["wind_speed"]
            desc = current["weather"][0]["description"]
            icon = current["weather"][0]["icon"]

            # --- DISPLAY LAYOUT ---
            st.header(f"Current Weather in Swindon")
            
            # Create three columns for a dashboard look
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Big weather icon
                st.image(f"http://openweathermap.org{icon}@4x.png")
                st.metric("Temperature", f"{round(temp, 1)}°C")
            
            with col2:
                st.write("") # Spacer
                st.metric("Feels Like", f"{round(feels_like, 1)}°C")
                st.metric("Humidity", f"{humidity}%")
            
            with col3:
                st.write("") # Spacer
                st.metric("Wind Speed", f"{round(wind_speed, 1)} m/s")
                st.metric("UV Index", uv_index)

            st.subheader(f"☁️ Condition: {desc.capitalize()}")
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
