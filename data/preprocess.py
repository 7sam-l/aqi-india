import pandas as pd
import numpy as np
from utils.aqi_calculator import get_aqi_from_pollutants, get_aqi_category

def process_latest_data(df):
    """
    Process latest measurements and calculate AQI.
    """
    if df.empty:
        return pd.DataFrame()
        
    df_final = df.copy()
    
    # Ensure all required pollutant columns exist and handle NaNs
    for p in ["pm25", "pm10", "no2", "co", "so2", "o3"]:
        if p not in df_final.columns:
            df_final[p] = np.nan
            
    # Calculate AQI and category
    df_final["aqi"] = df_final.apply(
        lambda row: get_aqi_from_pollutants(
            pm25=row["pm25"], 
            pm10=row["pm10"], 
            no2=row["no2"], 
            co=row["co"], 
            so2=row["so2"], 
            o3=row["o3"]
        ), axis=1
    )
    
    # Add category and color
    df_final[["category", "color"]] = df_final.apply(
        lambda row: pd.Series(get_aqi_category(row["aqi"])), axis=1
    )
    
    return df_final

def process_historical_data(df):
    """
    Process historical data for Prophet forecasting.
    Expects df with columns 'date', 'value', 'parameter'.
    """
    if df.empty:
        return pd.DataFrame()
        
    # Convert date to datetime
    df["ds"] = pd.to_datetime(df["date"])
    # Sort by date
    df = df.sort_values("ds")
    
    # Since OpenAQ gives multiple readings per day, we group by day
    df["ds"] = df["ds"].dt.date
    df_daily = df.groupby("ds")["value"].mean().reset_index()
    
    # Calculate AQI just for PM2.5 (as a simplification for historical data)
    df_daily["y"] = df_daily["value"].apply(
        lambda x: get_aqi_from_pollutants(pm25=x)
    )
    
    # Prophet requires ds to be datetime and y to be numeric
    df_daily["ds"] = pd.to_datetime(df_daily["ds"])
    
    return df_daily[["ds", "y"]]
