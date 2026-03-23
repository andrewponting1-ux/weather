import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track():
    st.set_page_config(page_title="Commute Optimizer", layout="centered")
    st.title("🌤️ My Local Weather Guide")

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
        
        # 1. BASE URL ONLY
        url = "https://api.openweathermap.org"
        
        # 2. SEPARATE PARAMETERS (More reliable for the cloud)
        params = {
            "lat": coords["lat"],
            "lon": coords["lon"],
            "appid": API_KEY,
            "units": "metric",
            "exclude": "minutely,hourly" # Simplifies the data coming back
        }
        
        # 3. REQUEST WITH PARAMS
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            temp = current["temp"]
            # Note: weather is a list, so we grab the first item [0]
            desc = current["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in {selected_city}")
            st.write(f"☁️ Condition: {desc.capitalize()}")
        
        elif response.status_code == 401:
            st.warning("⏳ Key not active yet. OpenWeather is still syncing your subscription.")
        else:
            st.error(f"⚠️ Server returned error: {response.status_code}")

    except Exception:
        # This keeps your key safe from logs
        st.error("📡 Network Error: Streamlit is struggling to reach the server. Try a quick 'Reboot' from the dashboard.")

    if st.button("🔄 Refresh"):
        st.rerun()
