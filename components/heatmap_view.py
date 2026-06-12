import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium

def render_heatmap(df):
    # df must have: lat, lon, aqi columns
    india_map = folium.Map(
        location=[22.5, 82.0],  # center of India
        zoom_start=5,
        tiles="CartoDB dark_matter"  # dark theme looks better for heatmaps
    )

    heat_data = []
    for _, row in df.iterrows():
        if row.get("lat") and row.get("lon") and row.get("aqi"):
            heat_data.append([row["lat"], row["lon"], row["aqi"]])

    HeatMap(
        heat_data,
        min_opacity=0.4,
        radius=35,
        blur=25,
        gradient={
            0.2: "green",
            0.4: "yellow",
            0.6: "orange",
            0.8: "red",
            1.0: "purple"
        }
    ).add_to(india_map)

    st_folium(india_map, width=900, height=500)
