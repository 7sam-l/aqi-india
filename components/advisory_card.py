import streamlit as st
import pandas as pd
from models.health_advisory import get_health_advisories

def render_advisory(city, df):
    """
    Renders a health advisory card based on the current AQI of the selected city.
    """
    if df.empty:
        st.info("Data not available for health advisory.")
        return
        
    city_data = df[df["city"] == city]
    
    if city_data.empty:
        st.info(f"No current AQI data available for {city}.")
        return
        
    # Get the AQI from the first matched row
    current_aqi = city_data.iloc[0].get("aqi", 0)
    category = city_data.iloc[0].get("category", "Unknown")
    
    advisory = get_health_advisories(current_aqi)
    
    st.markdown(f"### {advisory['icon']} Current Status: {category} (AQI: {current_aqi})")
    
    # Use Streamlit columns for a nicer layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**General Public:**")
        st.info(advisory["general"])
        
        st.markdown("**Outdoor Workers:**")
        st.warning(advisory["workers"])
        
    with col2:
        st.markdown("**Sensitive Groups (Children, Elderly, Asthmatics):**")
        st.error(advisory["sensitive"])
        
    # Show breakdown of current pollutants
    st.markdown("#### Current Pollutants")
    cols = st.columns(4)
    pollutants = ["pm25", "pm10", "no2", "co"]
    for i, p in enumerate(pollutants):
        val = city_data.iloc[0].get(p, "N/A")
        if pd.isna(val):
            val = "N/A"
        cols[i].metric(label=p.upper(), value=val)
