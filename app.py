import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track():
    st.set_page_config(page_title="My Local Weather", layout="centered")
    st.title("🌤️ My Local Weather Guide")

    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    try:
        # Using the One Call 3.0 format you found
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # Adding &units=metric so it shows Celsius
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # One Call puts current weather inside 'current'
            current = data["current"]
            temp = current["temp"]
            desc = current["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            
            if temp < 10:
                st.info("🧥 Chilly out there! Dress warmly.")
            else:
                st.success("✅ Weather looks good!")

        elif response.status_code == 401:
            st.error("Invalid API Key. Make sure you have 'One Call 3.0' activated in your account.")
        else:
            st.error(f"Error {response.status_code}. Check if you added a payment method to OpenWeather (they need it for 3.0, even the free part).")

    except Exception as e:
        st.error(f"⚠️ Connection error. The cloud is struggling to reach the server.")
