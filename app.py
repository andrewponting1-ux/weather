import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

st.title("🛡️ Ultimate Connection Test")

try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    
    # 1. SETUP A "RETRY" SESSIONimport streamlit as st
import requests
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track():
    st.set_page_config(page_title="Swindon Weather", layout="centered")
    st.title("🌤️ Swindon Weather Guide")

    # 1. SETTINGS
    LAT = 51.5558
    LON = -1.7797

    # 2. SECURE API CALL
    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
        
        # This is the EXACT URL from the 3.0 docs you provided
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        
        # We add these headers to make the request look like a real browser
        # This is often the "secret sauce" to unblock Streamlit Cloud
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["current"]["temp"]
            desc = data["current"]["weather"][0]["description"]
            
            st.header(f"{round(temp, 1)}°C in Swindon")
            st.write(f"☁️ Condition: {desc.capitalize()}")
            st.success("✅ Connection Successful!")
            st.balloons()
            
        elif response.status_code == 401:
            st.warning("⏳ Key not active: OpenWeather is still verifying your 3.0 subscription.")
        else:
            st.error(f"❌ Server Error {response.status_code}: {response.text}")

    except Exception:
        # SECURE: No variables here to protect your key from logs
        st.error("📡 Connection still blocked. Streamlit Cloud cannot reach the server.")

    # This forces the cloud to try multiple times before giving up
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    # 2. TEST URL
    url = f"https://api.openweathermap.org{API_KEY}"
    
    # 3. ATTEMPT CONNECTION
    # We use the 'session' instead of 'requests.get'
    response = session.get(url, timeout=20)
    
    if response.status_code == 200:
        st.success("🎉 SUCCESS! The network wall has been bypassed.")
        st.balloons()
    elif response.status_code == 401:
        st.warning("⏳ KEY NOT READY: Your network is fine, but the key is still activating (wait 1 hour).")
    else:
        st.error(f"❌ SERVER ERROR {response.status_code}")

except Exception as e:
    # We show the error name only, not the full URL or key
    error_type = type(e).__name__
    st.error(f"📡 Still Blocked: {error_type}")
    st.info("Tip: If you see 'NameResolutionError', Streamlit Cloud's DNS is down. Try changing Python version in Settings.")
