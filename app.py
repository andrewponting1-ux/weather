import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. PAGE CONFIG
st.set_page_config(page_title="UK Weather Guide", page_icon="🌤️", layout="centered")

# 2. DEFINE LOCATIONS (City: [Lat, Lon])
LOCATIONS = {
    "Swindon": [51.5558, -1.7797],
    "London": [51.5074, -0.1278],
    "Bristol": [51.4545, -2.5879],
    "Oxford": [51.7520, -1.2577],
    "Manchester": [53.4808, -2.2426]
}

# 3. CACHED API FUNCTION
@st.cache_data(ttl=600)
def get_weather(lat, lon, api_key):
    # Note: Ensure your subscription supports the 3.0 One Call API
    url = f"https://api.openweathermap.org{lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        return response
    except Exception:
        return None

# 4. TRACKING & UI
with streamlit_analytics.track():
    st.title("🌤️ UK Weather Guide")

    # DROPDOWN SELECTOR
    selected_city = st.selectbox("Select a Location:", list(LOCATIONS.keys()))
    coords = LOCATIONS[selected_city]

    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        response = get_weather(coords[0], coords[1], API_KEY)
        
        if response and response.status_code == 200:
            data = response.json()
            current = data["current"]
            temp = current["temp"]
            desc = current["weather"][0]["description"]
            icon = current["weather"][0]["icon"]
            
            # Display results
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(f"http://openweathermap.org{icon}@4x.png")
            with col2:
                st.header(f"{round(temp, 1)}°C in {selected_city}")
                st.subheader(desc.capitalize())
            
            st.success(f"✅ Live data for {selected_city}")
            
        elif response and response.status_code == 401:
            st.warning("⏳ API Key not active or invalid for One Call 3.0.")
        else:
            st.error(f"❌ Connection Failed (Error {response.status_code if response else 'Unknown'})")

    except KeyError:
        st.error("🔑 Missing 'OPENWEATHER_API_KEY' in Streamlit Secrets.")

    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()
