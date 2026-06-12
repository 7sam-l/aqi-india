import streamlit as st
import pandas as pd
from data.fetch_data import fetch_latest_india
from data.preprocess import process_latest_data
from components.map_view import render_map
from components.chart_view import render_trend_chart, render_forecast_chart
from components.advisory_card import render_advisory

# Page Config
st.set_page_config(page_title="AQI India Dashboard", layout="wide", page_icon="🌫️")

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    h1, h2, h3 {
        color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌫️ India Air Quality Dashboard")
st.markdown("Real-time AQI tracking and 7-day forecasting for major Indian cities.")

# Load fallback cities list
@st.cache_data
def load_cities():
    try:
        df = pd.read_csv("data/cities.csv")
        return df["city"].tolist()
    except:
        return ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata"]

fallback_cities = load_cities()

# Sidebar
st.sidebar.header("Settings")

# Fetch and process live data
with st.spinner("Fetching live AQI data from OpenAQ..."):
    raw_df = fetch_latest_india()
    df = process_latest_data(raw_df)

# Get list of available cities from live data, fallback if empty
if not df.empty:
    available_cities = sorted(df["city"].unique().tolist())
    # Add fallback cities if they are missing
    for c in fallback_cities:
        if c not in available_cities:
            available_cities.append(c)
    available_cities = sorted(list(set(available_cities)))
else:
    available_cities = sorted(fallback_cities)

# Default to Delhi if present, else first in list
default_index = available_cities.index("Delhi") if "Delhi" in available_cities else 0
selected_city = st.sidebar.selectbox("Select City", available_cities, index=default_index)
show_forecast = st.sidebar.checkbox("Show 7-day Forecast", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**About this app:**")
st.sidebar.markdown("Built with Streamlit, Prophet, and Folium. Data provided by OpenAQ.")

# Map Section
st.subheader("Live AQI Map")
if not df.empty:
    render_map(df)
else:
    st.warning("Could not load live AQI map. OpenAQ API might be temporarily unavailable.")

st.markdown("---")

# City Detail Section
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Historical Trend — {selected_city}")
    render_trend_chart(selected_city)

with col2:
    if show_forecast:
        st.subheader("7-Day Forecast")
        render_forecast_chart(selected_city)

st.markdown("---")

# Health Advisory Section
st.subheader("Health Advisory")
if not df.empty:
    render_advisory(selected_city, df)
else:
    st.info("Health advisory requires live AQI data.")

st.markdown("---")
st.caption("Data source: OpenAQ API. AQI calculated using CPCB sub-index method. Forecast generated using Prophet.")
