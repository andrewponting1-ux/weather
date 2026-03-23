import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track():
    st.set_page_config(page_title="Commute Optimizer", layout="centered")
    st.title("🚲 Commute Optimizer")

    CITIES = {
        "Bristol": {"lat": 51.4545, "lon": -2.5879},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Manchester": {"lat": 53.4808, "lon": -2.2426},
        "Swindon": {"lat": 51.5558, "lon": -1.7797}
    }

    selected_city = st.selectbox("📍 Select Location:", list(CITIES.keys()))
    coords = CITIES[selected_city]

    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        url = f"https://api.openweathermap.org{coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"
        
        # 1. MAKE THE API CALL (This creates 'response')
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # 2. CURRENT WEATHER
            current = data["current"]
            temp = current["temp"]
            description = current["weather"][0]["description"]
            summary = data["daily"][0].get("summary", "No summary available.")

            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.subheader(summary)
            
            # 3. RAIN CHART DATA
            hourly_data = data["hourly"]
            chart_list = []
            for hour in hourly_data[:24]: # Just show the next 24 hours for better mobile view
                chart_list.append({
                    "Time": datetime.fromtimestamp(hour["dt"]).strftime("%H:00"),
                    "Rain Chance (%)": hour.get("pop", 0) * 100
                })
            
            df = pd.DataFrame(chart_list)
            st.divider()
            st.subheader("🌧️ Rain Probability (Next 24h)")
            st.bar_chart(df.set_index("Time"))

        else:
            st.error(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(f"Connection failed: {e}")
