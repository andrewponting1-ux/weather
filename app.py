import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="My Local Weather", layout="centered")
    st.title("🌤️ My Local Weather Guide")
    st.markdown("Secure Weather & Air Quality Advice")

    # 2. LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 3. ACCESSING THE SECRET KEY (Safe way)
    # This looks for 'OPENWEATHER_API_KEY' in your Streamlit Cloud Settings
    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # 4. FETCH DATA FROM OPENWEATHERMAP
        # Units=metric gives us Celsius instead of Fahrenheit
        url = f"https://api.openweathermap.org{lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            
            # Display the info
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            st.write(f"💧 Humidity: {humidity}%")
            
            # Simple Advice
            if temp < 10:
                st.info(f"🧥 It's chilly in {selected_city}. Dress warmly!")
            elif "rain" in desc.lower():
                st.warning(f"☔ Rain in {selected_city}. Take an umbrella!")
            else:
                st.success(f"✅ Looking good in {selected_city}!")
                
        elif response.status_code == 401:
            st.error("Invalid API Key. Please check your Secrets in Streamlit Cloud.")
        else:
            st.error(f"Weather server error: {response.status_code}")

    except KeyError:
        st.warning("⚠️ API Key not found! Please add 'OPENWEATHER_API_KEY' to your Streamlit Cloud Secrets.")
    except Exception as e:
        st.error("⚠️ Connection failed. Please try refreshing in a moment.")
