import streamlit as st
import requests

st.title("🧪 Connection Check-Up")

# 1. Check if the Secret even exists in Streamlit Cloud
if "OPENWEATHER_API_KEY" not in st.secrets:
    st.error("❌ KEY MISSING: I can't find 'OPENWEATHER_API_KEY' in your Streamlit Secrets box.")
else:
    st.success("✅ SECRET FOUND: Your app can see the key in the vault.")
    
    # 2. Try a direct connection test
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    test_url = f"https://api.openweathermap.org{API_KEY}"
    
    try:
        res = requests.get(test_url, timeout=10)
        if res.status_code == 200:
            st.success("🎉 IT WORKS! The weather server accepted your key.")
            st.balloons()
        elif res.status_code == 401:
            st.warning("⏳ KEY NOT READY: The server says your key is invalid. Please wait 1-2 hours for it to activate.")
        else:
            st.error(f"🌐 SERVER ERROR {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"📡 NETWORK BLOCKED: Streamlit Cloud cannot reach the server at all.")
