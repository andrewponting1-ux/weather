import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING
with streamlit_analytics.track():
    st.title("🌤️ My Local Weather Guide") 
    st.markdown("Simple Weather Advice")

    # 2. LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 3. THE "FAKE BROWSER" HEADER
    # This makes the request look like it's from a real person, not a bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 4. FETCH DATA
    try:
        # We use the simplest possible URL to avoid errors
        url = f"https://api.open-meteo.com{lat}&longitude={lon}&current_weather=true"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["current_weather"]["temperature"]
            wind = data["current_weather"]["windspeed"]
            
            st.header(f"Current Temp: {temp}°C")
            st.write(f"Wind Speed: {wind} km/h")
            
            if temp < 10:
                st.info(f"🧥 It's chilly in {selected_city} today!")
            else:
                st.success(f"☀️ Looking good in {selected_city}!")
        else:
            st.error(f"Error: The server said '{response.status_code}'. This usually means Streamlit is being blocked.")

    except Exception as e:
        st.error("⚠️ Connection failed. Please try refreshing the page in a few seconds.")

