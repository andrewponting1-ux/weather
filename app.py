import streamlit as st
import requests

st.title("🛡️ API Safety Tester")

try:
    # Pull key from your Secret vault
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    
    # We use a standard 'ping' to the 2.5 API as a test 
    # (2.5 is faster to activate than 3.0)
    test_url = f"https://api.openweathermap.org{API_KEY}"
    
    response = requests.get(test_url, timeout=10)
    
    if response.status_code == 200:
        st.success("✅ SUCCESS: Your API key is live and working!")
        st.balloons()
    elif response.status_code == 401:
        st.warning("⏳ NOT READY: Your key exists, but OpenWeather hasn't activated it yet. Wait 1-2 hours.")
    else:
        st.error(f"❌ SERVER ERROR {response.status_code}: The server is reachable but rejected the request.")

except Exception:
    # SECURE: This catch-all hides all technical details including your API key
    st.error("📡 NETWORK BLOCKED: Streamlit Cloud cannot reach the weather server at all.")
