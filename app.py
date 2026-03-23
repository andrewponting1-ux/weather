import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. TRACKING
with streamlit_analytics.track():
    st.title("🌤️ My Local Weather Guide") 
    st.markdown("Custom Weather & Air Quality Advice")

    # 2. LOCATIONS
    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426}
    }

    selected_city = st.selectbox("📍 Choose a city:", list(CITIES.keys()))
    lat, lon = CITIES[selected_city]["lat"], CITIES[selected_city]["lon"]

    # 3. THE "HEADER" TRICK (Fixes most connection errors)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    # 4. FETCH DATA
    try:
        # Weather URL
        w_url = f"https://api.open-meteo.com{lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(w_url, headers=headers, timeout=10)
        
        if w_res.status_code == 200:
            data = w_res.json()
            temp = data["current_weather"]["temperature"]
            st.header(f"Current Temp: {temp}°C")
            
            # Simple Advice
            if temp < 10:
                st.info("🧥 It's a bit chilly in " + selected_city + ". Wear a coat!")
            else:
                st.success("😎 Nice weather for a walk!")
        else:
            st.error(f"Weather server responded with error: {w_res.status_code}")

    except Exception as e:
        st.error("⚠️ Connection failed. The weather server might be busy. Please refresh the page.")

    # 5. OPTIONAL: AIR QUALITY (Separate so it doesn't break the weather)
    try:
        a_url = f"https://air-quality-api.open-meteo.com{lat}&longitude={lon}&current=european_aqi"
        a_res = requests.get(a_url, headers=headers, timeout=10)
        if a_res.status_code == 200:
            aqi = a_res.json()["current"]["european_aqi"]
            st.write(f"Air Quality (AQI): {aqi}")
    except:
        st.write("Air Quality data is taking a break...")
