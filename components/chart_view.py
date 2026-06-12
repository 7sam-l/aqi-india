import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data.fetch_data import fetch_historical_city_data
from data.preprocess import process_historical_data
from models.forecast import forecast_aqi

def render_trend_chart(city):
    """
    Renders a 30-day historical trend chart for AQI.
    """
    # Fetch 30 days of data for trend
    df_raw = fetch_historical_city_data(city, days=30)
    
    if df_raw.empty:
        st.info("No historical data available for this city.")
        return
        
    df = process_historical_data(df_raw)
    
    if df.empty:
        st.info("Could not process historical data.")
        return
        
    fig = px.line(df, x="ds", y="y", title="30-Day AQI Trend (PM2.5 equivalent)")
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="AQI",
        hovermode="x unified"
    )
    
    # Add colored bands for AQI categories
    fig.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.1, layer="below", line_width=0)
    fig.add_hrect(y0=51, y1=100, fillcolor="yellow", opacity=0.1, layer="below", line_width=0)
    fig.add_hrect(y0=101, y1=200, fillcolor="orange", opacity=0.1, layer="below", line_width=0)
    fig.add_hrect(y0=201, y1=300, fillcolor="red", opacity=0.1, layer="below", line_width=0)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Render best and worst day highlights
    render_best_worst(df, city)

def render_best_worst(city_df, city_name):
    # Handle both column naming conventions
    aqi_col = "aqi" if "aqi" in city_df.columns else "y"
    date_col = "date" if "date" in city_df.columns else "ds"
    
    worst = city_df.loc[city_df[aqi_col].idxmax()]
    best = city_df.loc[city_df[aqi_col].idxmin()]

    col1, col2 = st.columns(2)
    with col1:
        st.error(f"🔴 Worst Day\n\n**{worst[date_col].strftime('%d %b %Y')}**\n\nAQI: {int(worst[aqi_col])}")
    with col2:
        st.success(f"🟢 Best Day\n\n**{best[date_col].strftime('%d %b %Y')}**\n\nAQI: {int(best[aqi_col])}")

def render_forecast_chart(city):
    """
    Renders a 7-day forecast chart using Prophet.
    """
    # Prophet needs more data to train well, so fetch 90 days
    df_raw = fetch_historical_city_data(city, days=90)
    
    if df_raw.empty:
        st.info("Not enough data to generate a forecast.")
        return
        
    df = process_historical_data(df_raw)
    
    with st.spinner("Generating 7-day forecast..."):
        forecast = forecast_aqi(df, periods=7)
        
    if forecast.empty:
        st.info("Forecast generation failed.")
        return
        
    fig = go.Figure()
    
    # Add historical data (last 14 days for context)
    df_recent = df.tail(14)
    fig.add_trace(go.Scatter(
        x=df_recent["ds"], y=df_recent["y"],
        mode="lines+markers",
        name="Historical AQI",
        line=dict(color="blue")
    ))
    
    # Add forecast line
    fig.add_trace(go.Scatter(
        x=forecast["ds"], y=forecast["yhat"],
        mode="lines+markers",
        name="Forecasted AQI",
        line=dict(color="red", dash="dash")
    ))
    
    # Add confidence interval
    fig.add_trace(go.Scatter(
        x=forecast["ds"].tolist() + forecast["ds"].tolist()[::-1],
        y=forecast["yhat_upper"].tolist() + forecast["yhat_lower"].tolist()[::-1],
        fill="toself",
        fillcolor="rgba(255, 0, 0, 0.2)",
        line=dict(color="rgba(255, 255, 255, 0)"),
        hoverinfo="skip",
        showlegend=True,
        name="Confidence Interval"
    ))
    
    fig.update_layout(
        title="7-Day AQI Forecast",
        xaxis_title="Date",
        yaxis_title="AQI",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
