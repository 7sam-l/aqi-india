import streamlit as st
import pandas as pd
from data.fetch_data import fetch_latest_india, fetch_historical_city_data
from data.preprocess import process_latest_data, process_historical_data
from components.map_view import render_map
from components.heatmap_view import render_heatmap
from components.chart_view import render_trend_chart, render_forecast_chart
from components.advisory_card import render_advisory
from components.compare_view import render_compare

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
    map_type = st.radio("Map Type", ["Markers", "Heatmap"], horizontal=True)
    if map_type == "Markers":
        render_map(df)
    else:
        render_heatmap(df)
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

# Compare Cities Section
st.subheader("🔁 Compare Two Cities")
col1, col2 = st.columns(2)
with col1:
    city_a = st.selectbox("City A", available_cities, key="city_a", index=available_cities.index(selected_city) if selected_city in available_cities else 0)
with col2:
    default_b = available_cities[1] if len(available_cities) > 1 else available_cities[0]
    city_b = st.selectbox("City B", available_cities, key="city_b", index=available_cities.index(default_b) if default_b in available_cities else 0)

if city_a != city_b:
    df_a_raw = fetch_historical_city_data(city_a, days=30)
    df_b_raw = fetch_historical_city_data(city_b, days=30)
    if not df_a_raw.empty and not df_b_raw.empty and not df.empty:
        df_a = process_historical_data(df_a_raw)
        df_b = process_historical_data(df_b_raw)
        
        city1_live = df[df["city"] == city_a].iloc[-1].to_dict() if not df[df["city"] == city_a].empty else {}
        city2_live = df[df["city"] == city_b].iloc[-1].to_dict() if not df[df["city"] == city_b].empty else {}
        
        render_compare(df_a, df_b, city1_live, city2_live, city_a, city_b)
    else:
        st.warning("Not enough historical data to compare these cities.")
else:
    st.warning("Please select two different cities.")

st.markdown("---")

# Health Advisory Section
st.subheader("Health Advisory")
if not df.empty:
    city_row = df[df["city"] == selected_city].iloc[-1].to_dict()
    render_advisory(selected_city, city_row)
else:
    st.info("Health advisory requires live AQI data.")

st.markdown("---")
st.caption("Data source: OpenAQ API. AQI calculated using CPCB sub-index method. Forecast generated using Prophet.")
