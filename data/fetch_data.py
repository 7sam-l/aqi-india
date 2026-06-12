import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_latest_india():
    """
    Fetches the latest AQI readings for locations in India using Open-Meteo API.
    """
    try:
        cities_df = pd.read_csv("data/cities.csv")
    except Exception as e:
        st.error("Could not load cities.csv")
        return pd.DataFrame()
        
    lats = ",".join(cities_df["lat"].astype(str))
    lons = ",".join(cities_df["lon"].astype(str))
    
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lats,
        "longitude": lons,
        "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # If there's only one city, open-meteo returns a dict. If multiple, it returns a list of dicts.
        if isinstance(data, dict):
            data = [data]
            
        records = []
        for i, item in enumerate(data):
            city_name = cities_df.iloc[i]["city"]
            current = item.get("current", {})
            records.append({
                "city": city_name,
                "lat": item["latitude"],
                "lon": item["longitude"],
                "pm25": current.get("pm2_5"),
                "pm10": current.get("pm10"),
                "no2": current.get("nitrogen_dioxide"),
                "co": current.get("carbon_monoxide"),
                "so2": current.get("sulphur_dioxide"),
                "o3": current.get("ozone"),
                "last_updated": current.get("time")
            })
            
        return pd.DataFrame(records)
        
    except Exception as e:
        st.error(f"Error fetching live data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=86400) # Cache historical data for 24 hours
def fetch_historical_city_data(city, days=90):
    """
    Fetches historical PM2.5 measurements for a specific city for the last N days.
    This is used for Prophet forecasting.
    """
    try:
        cities_df = pd.read_csv("data/cities.csv")
        city_row = cities_df[cities_df["city"] == city]
        if city_row.empty:
            st.error(f"Coordinates for {city} not found.")
            return pd.DataFrame()
            
        lat = city_row.iloc[0]["lat"]
        lon = city_row.iloc[0]["lon"]
    except Exception as e:
        st.error("Could not load cities.csv")
        return pd.DataFrame()

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5",
        "past_days": days
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        pm25 = hourly.get("pm2_5", [])
        
        records = []
        for t, v in zip(times, pm25):
            if v is not None:
                records.append({
                    "date": t,
                    "value": v,
                    "parameter": "pm25"
                })
            
        return pd.DataFrame(records)
        
    except Exception as e:
        st.error(f"Error fetching historical data for {city}: {e}")
        return pd.DataFrame()
