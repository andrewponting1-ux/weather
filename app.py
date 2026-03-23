import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. PAGE CONFIG
st.set_page_config(page_title="UK Weather Guide", page_icon="🌤️", layout="centered")

# 2. LOCATIONS DICTIONARY
LOCATIONS = {
    "Swindon": {"lat": 51.5558, "lon": -1.7797},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Bristol": {"lat": 51.4545, "lon": -2.5879},
    "Oxford": {"lat": 51.7520, "lon": -1.2577}
}

# 3. WEATHER FETCH FUNCTION
@st.cache_data(ttl=600)
def get_weather(lat, lon, api_key):
    # One Call 3.0 URL
    url = f"https://api.openweathermap.org{lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        return response
    except Exception:
        return None

# 4. APP UI
with streamlit_analytics.track():
    st.title("🌤️ UK Weather Guide")

    # Dropdown to pick location
    selected_city = st.selectbox("Select a Location:", list(LOCATIONS.keys()))
    city_data = LOCATIONS[selected_city]

    try:
        # Check for Secret
        if "OPENWEATHER_API_KEY" not in st.secrets:
            st.error("🔑 Missing Secret: Add 'OPENWEATHER_API_KEY' to your Streamlit Cloud Secrets.")
        else:
            API_KEY = st.secrets["OPENWEATHER_API_KEY"]
            response = get_weather(city_data["lat"], city_data["lon"], API_KEY)
            
            if response and response.status_code == 200:
                data = response.json()
                current = data["current"]
                
                # Extracting specific fields (Note the [0] for weather list)
                temp = current["temp"]
                desc = current["weather"][0]["description"]
                icon = current["weather"][0]["icon"]

                # Display columns
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(f"http://openweathermap.org{icon}@4x.png")
                with col2:
                    st.header(f"{round(temp, 1)}°C")
                    st.subheader(desc.capitalize())
                    st.write(f"📍 Showing weather for **{selected_city}**")
                
            elif response and response.status_code == 401:
                st.warning("⚠️ **Subscription Error (401):** Ensure you have active 'One Call 3.0' access in your OpenWeather dashboard.")
            else:
                error_code = response.status_code if response else "Connection Timeout"
                st.error(f"❌ Connection Failed (Error {error_code}). Check your internet or API subscription.")

    except Exception as e:
        st.error(f"📡 An unexpected error occurred: {e}")

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
