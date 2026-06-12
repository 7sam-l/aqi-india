# AQI India — Real-Time Air Quality Dashboard

A full-stack data science web application that shows real-time AQI across Indian cities on an interactive map, predicts health risk, and forecasts AQI for the next 7 days using time series modeling.

## Features
- **Real-Time AQI Map**: Live data fetched from Open-Meteo Air Quality API displayed on a color-coded interactive map.
- **Historical Trends**: 30-day historical trends of PM2.5 and AQI.
- **7-Day Forecast**: Future AQI predictions utilizing Meta's Prophet time series model.
- **Health Advisories**: Rule-based system for sensitive groups, workers, and the general public based on CPCB formulas.

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Tech Stack
- **Framework:** Streamlit
- **Data & Forecasting:** Pandas, NumPy, Scikit-learn, Prophet
- **Visualizations:** Plotly, Folium, streamlit-folium
- **Data Source:** Open-Meteo Air Quality API
