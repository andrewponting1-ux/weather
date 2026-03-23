import streamlit as st
import requests
import pandas as pd
from streamlit_folium import st_folium
import folium
import streamlit_analytics2 as streamlit_analytics


# 1. Start Analytics (Add ?analytics=on to your URL to see stats)
with streamlit_analytics.track():
    st.set_page_config(page_title="SHIFT Commute", page_icon="🚲")

    st.title("🚲 SHIFT: Commute Optimizer")
    st.caption("Weather • Air Quality • Pollen • Travel Advice")

    # 2. Location Picker (Default Swindon)
    if 'lat' not in st.session_state:
        st.session_state.lat, st.session_state.lon = 51.5581, -1.7819

    with st.expander("📍 Tap map to change location"):
        m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=10)
        m.add_child(folium.LatLngPopup())
        map_data = st_folium(m, height=250, width=700)
        if map_data['last_clicked']:
            st.session_state.lat = map_data['last_clicked']['lat']
            st.session_state.lon = map_data['last_clicked']['lng']

    # 3. Fetch All Data (Cached for 1 hour to save API hits)
    @st.cache_data(ttl=3600)
    def get_data(lat, lon):
        w_url = f"https://api.open-meteo.com{lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,precipitation_probability&forecast_days=1"
        # Includes Birch, Grass, and Ragweed pollen
        a_url = f"https://air-quality-api.open-meteo.com{lat}&longitude={lon}&current=european_aqi,birch_pollen,grass_pollen&forecast_days=1"
        return requests.get(w_url).json(), requests.get(a_url).json()

    try:
        w, a = get_data(st.session_state.lat, st.session_state.lon)
        
        # 4. Dashboard Metrics
        cols = st.columns(3)
        cols[0].metric("Temp", f"{w['current']['temperature_2m']}°C")
        cols[1].metric("Air Quality", f"{a['current']['european_aqi']} AQI")
        
        pollen_sum = a['current']['birch_pollen'] + a['current']['grass_pollen']
        cols[2].metric("Pollen", "High" if pollen_sum > 15 else "Low")

        # 5. THE SHIFT ADVICE
        st.subheader("🎒 Your Commute Bag")
        
        # Rain/Gear Logic
        if w['hourly']['precipitation_probability'][0] > 25:
            st.error("Pack an Umbrella! ☂️")
        elif w['current']['temperature_2m'] < 12:
            st.info("Wear a Heavy Coat 🧥")
        else:
            st.success("Light Jacket is fine 🧥")

        # Allergy/Health Logic
        if pollen_sum > 10:
            st.warning("Pollen is active: Take an Antihistamine 💊")
        if a['current']['european_aqi'] > 60:
            st.warning("Pollution is high: Avoid deep breaths near traffic 😷")

        # Travel Logic
        if w['current']['wind_speed_10m'] > 25:
            st.write("**Travel Mode:** Take the Bus/Train 🚌 (Too windy for cycling)")
        else:
            st.write("**Travel Mode:** Perfect for a Bike or Walk! 🚲")

        # 6. Visual Graph
        st.subheader("📈 Temperature Next 24h")
        df = pd.DataFrame({"Hour": range(24), "Temp": w['hourly']['temperature_2m']})
        st.line_chart(df.set_index("Hour"))

    except:
        st.write("Connect to internet to load weather data.")
