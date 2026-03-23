import streamlit as st
import requests

st.title("🌤️ Weather Test")

# This pulls from your Streamlit Cloud "Secrets" box
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# Using the standard 2.5 version (no credit card needed)
# Notice the '?' and the '&' - these must be exactly right!
url = f"https://api.openweathermap.org{API_KEY}&units=metric"

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        st.success(f"✅ Connection Successful! Bristol is {temp}°C")
    else:
        # This will tell us if the key is invalid or the plan is wrong
        st.error(f"❌ Server error {response.status_code}: {response.text}")

except Exception as e:
    st.error(f"⚠️ Connection failed: {e}")
