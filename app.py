import streamlit as st
import requests

# 1. SETUP
st.set_page_config(page_title="UK Weather", page_icon="🌤️")

LOCATIONS = {
    "Swindon": {"lat": 51.5558, "lon": -1.7797},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Bristol": {"lat": 51.4545, "lon": -2.5879}
}

# 2. UI
st.title("🌤️ UK Weather Guide")
selected_city = st.selectbox("Select a Location:", list(LOCATIONS.keys()))
city = LOCATIONS[selected_city]

# 3. WEATHER FETCH (Using the standard 2.5 API for better compatibility)
if "OPENWEATHER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    
    # Standard Current Weather API URL (more reliable for free keys)
    url = f"https://api.openweathermap.org{city['lat']}&lon={city['lon']}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5) # 5 second limit
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(f"http://openweathermap.org{icon}@4x.png")
            with col2:
                st.header(f"{round(temp, 1)}°C")
                st.subheader(desc.title())
                st.write(f"Showing live data for {selected_city}")
        
        elif response.status_code == 401:
            st.error("🔑 API Key is invalid or not yet active. (New keys can take 2 hours to work).")
        else:
            st.error(f"❌ Server returned error {response.status_code}")

    except Exception:
        st.error("📡 Connection Timeout. Your network might be blocking the weather service.")
else:
    st.warning("⚠️ Please add your OPENWEATHER_API_KEY to Streamlit Secrets.")
