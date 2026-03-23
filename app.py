import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Swindon Weather", page_icon="🌤️", layout="centered")

# 2. CACHED API FUNCTION (Saves API calls & speeds up the app)
@st.cache_data(ttl=600)  # Refresh data every 10 minutes
def get_weather_data(api_key):
    # Swindon Coordinates
    LAT, LON = 51.5558, -1.7797
    PART = "minutely,hourly,daily,alerts"
    
    # Corrected f-string URL with metric units
    url = f"https://api.openweathermap.org{LAT}&lon={LON}&exclude={PART}&appid={api_key}&units=metric"
    
    headers = {'User-Agent': 'SwindonWeatherApp/1.0'}
    response = requests.get(url, headers=headers, timeout=10)
    return response

# 3. ANALYTICS & UI
with streamlit_analytics.track():
    st.title("🌤️ Swindon Weather Guide")

    try:
        # Securely pull your API key
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        response = get_weather_data(API_KEY)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract data points
            current = data["current"]
            temp = current["temp"]
            desc = current["weather"][0]["description"]
            icon_code = current["weather"][0]["icon"]
            wind_ms = current["wind_speed"]
            
            # Convert wind speed from m/s to MPH (standard for UK)
            wind_mph = wind_ms * 2.237

            # Layout: Display Icon and Temp side-by-side
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # OpenWeather official icon URL
                icon_url = f"http://openweathermap.org{icon_code}@4x.png"
                st.image(icon_url)
            
            with col2:
                st.markdown(f"## {round(temp, 1)}°C")
                st.markdown(f"### {desc.capitalize()}")
                st.write(f"💨 **Wind:** {round(wind_mph, 1)} mph")

            st.success("✅ Live Data from OpenWeather 3.0")
            
        elif response.status_code == 401:
            st.error("🔑 **API Key Error:** Ensure your One Call 3.0 subscription is active in the [OpenWeather Dashboard](https://home.openweathermap.org).")
        else:
            st.error(f"❌ **Server Error {response.status_code}:** {response.reason}")

    except KeyError:
        st.error("⚠️ **Secret Missing:** Please add `OPENWEATHER_API_KEY` to your Streamlit Cloud Secrets.")
    except Exception as e:
        st.error("📡 **Connection Error:** Could not reach weather service.")

    # Refresh Button
    if st.button("🔄 Check Latest Weather"):
        st.cache_data.clear() # Clears the 10-minute cache to force a new pull
        st.rerun()
