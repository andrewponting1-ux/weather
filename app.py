import streamlit as st
import pandas as pd
from datetime import datetime

# ... (keep your existing imports and API call code)

if response.status_code == 200:
    data = response.json()
    
    # 1. Prepare data for the chart
    # 'hourly' contains 48 objects; we extract 'dt' (time) and 'pop' (probability)
    hourly_data = data["hourly"]
    
    chart_data = []
    for hour in hourly_data:
        chart_data.append({
            "Time": datetime.fromtimestamp(hour["dt"]).strftime("%H:%M (%a)"),
            "Rain Probability (%)": hour.get("pop", 0) * 100
        })
    
    # Convert to a DataFrame for Streamlit
    df = pd.DataFrame(chart_data)

    # 2. Display the Chart
    st.divider()
    st.subheader("🌧️ 48-Hour Rain Forecast")
    st.write("Chance of rain for your commute over the next 2 days:")
    
    # Creating the bar chart
    st.bar_chart(df.set_index("Time"))

    # 3. Peak Rain Warning
    max_pop = df["Rain Probability (%)"].max()
    if max_pop > 50:
        peak_time = df.loc[df["Rain Probability (%)"].idxmax(), "Time"]
        st.warning(f"⚠️ High risk of rain ({round(max_pop)}%) peak expected around {peak_time}.")
