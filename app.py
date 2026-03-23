import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

st.title("🛡️ Ultimate Connection Test")

try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    
    # 1. SETUP A "RETRY" SESSION
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
