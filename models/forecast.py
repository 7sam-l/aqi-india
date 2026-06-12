import pandas as pd
from prophet import Prophet
import streamlit as st

@st.cache_data(ttl=86400) # Cache the forecast for 24 hours
def forecast_aqi(city_df, periods=7):
    """
    Trains a Prophet model on the given city_df and forecasts for the specified periods.
    city_df must have columns: ds (datetime), y (AQI value)
    """
    if city_df.empty or len(city_df) < 14: # Require at least 2 weeks of data
        return pd.DataFrame()
        
    try:
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05
        )
        
        # Suppress logging
        import logging
        logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
        
        model.fit(city_df)
        
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        # We only want the future predictions
        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
        
    except Exception as e:
        st.error(f"Error forecasting AQI: {e}")
        return pd.DataFrame()
