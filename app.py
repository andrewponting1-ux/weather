import streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

# 1. SETTINGS & LOCATIONS
LOCATIONS = {
    "Swindon": {"lat": 51.5558, "lon": -1.7797},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Bristol": {"lat": 51.4545, "lon": -2.5879},
    "Oxford": {"lat": 51.7520, "lon": -1.2577}
}

# 2. TRACKING & PAGE CONFIG
with streamlit_analytics.track():
    st.set_page_config(page_title="UK Weather Guide", layout="centered")
    st.title("🌤️ UK Weather Guide")

    # Dropdown for locations
    selected_city = st.selectbox("Select a Location:", list(LOCATIONS.keys()))
    city = LOCATIONS[selected_city]

    # 3. SECURE API CALL (Standard 2.5 API)
    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # Use the standard 2.5 weather URL - much more reliable for free keys
        url = f"https://api.openweathermap.org{city['lat']}&lon={city['lon']}&appid={API_KEY}&units=metric"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Data parsing for 2.5 structure
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            
            # Display results
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(f"http://openweathermap.org{icon}@4x.png")
            with col2:
                st.header(f"{round(temp, 1)}°C in {selected_city}")
                st.write(f"☁️ Condition: {desc.capitalize()}")
                st.success("✅ Connection Successful!")
            
        elif response.status_code == 401:
            st.warning("⏳ Key issue. OpenWeather may still be syncing your account.")
        else:
            st.error(f"❌ Server Error {response.status_code}. Using the standard 2.5 API.")

    except Exception as e:
        st.error("📡 Connection blocked or timeout. Check your Streamlit Secrets.")

    if st.button("🔄 Refresh"):
        st.rerun()
