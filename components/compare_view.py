import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_compare(city1_hist, city2_hist, city1_live, city2_live, city1_name, city2_name):
    col1, col2 = st.columns(2)

    for col, hist_df, live_row, name in [(col1, city1_hist, city1_live, city1_name), (col2, city2_hist, city2_live, city2_name)]:
        with col:
            current_aqi = live_row.get("aqi", 0)
            # Use "y" for historical AQI (from Prophet preprocessing)
            avg_7day = hist_df["y"].tail(7).mean() if "y" in hist_df.columns else 0
            
            pollutants = {
                "pm25": live_row.get("pm25", 0), 
                "pm10": live_row.get("pm10", 0), 
                "no2": live_row.get("no2", 0)
            }
            # Filter out NaNs to find the max safely
            pollutants = {k: v for k, v in pollutants.items() if pd.notna(v)}
            worst_pollutant = max(pollutants, key=pollutants.get) if pollutants else "N/A"

            st.metric(label=f"{name} — Current AQI", value=int(current_aqi))
            st.metric(label="7-Day Average", value=round(avg_7day, 1))
            st.metric(label="Worst Pollutant Today", value=worst_pollutant.upper())

    # Overlapping trend chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=city1_hist["ds"] if "ds" in city1_hist.columns else city1_hist["date"], 
        y=city1_hist["y"] if "y" in city1_hist.columns else city1_hist["aqi"],
        name=city1_name, line=dict(color="royalblue", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=city2_hist["ds"] if "ds" in city2_hist.columns else city2_hist["date"], 
        y=city2_hist["y"] if "y" in city2_hist.columns else city2_hist["aqi"],
        name=city2_name, line=dict(color="tomato", width=2)
    ))
    fig.update_layout(
        title="AQI Trend Comparison (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="AQI",
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
