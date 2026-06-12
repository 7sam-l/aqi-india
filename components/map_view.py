import folium
from streamlit_folium import st_folium

def render_map(df):
    """
    Renders a Folium map with city markers colored by AQI.
    """
    # Center map on India
    india_center = [22.0, 79.0]
    m = folium.Map(location=india_center, zoom_start=5, tiles="CartoDB positron")
    
    if df.empty:
        st_folium(m, width=800, height=500)
        return
        
    for idx, row in df.iterrows():
        # Get appropriate color map
        color = row.get("color", "gray")
        
        # Build popup HTML
        html = f"""
        <div style="font-family: Arial; min-width: 150px;">
            <h4 style="margin-bottom: 5px;">{row['city']}</h4>
            <b>AQI:</b> {row.get('aqi', 'N/A')} ({row.get('category', 'Unknown')})<br/>
            <hr style="margin: 5px 0;">
            <small>
            <b>PM2.5:</b> {row.get('pm25', 'N/A')}<br/>
            <b>PM10:</b> {row.get('pm10', 'N/A')}<br/>
            <b>NO2:</b> {row.get('no2', 'N/A')}<br/>
            <b>CO:</b> {row.get('co', 'N/A')}<br/>
            </small>
        </div>
        """
        iframe = folium.IFrame(html=html, width=200, height=160)
        popup = folium.Popup(iframe, max_width=200)
        
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            popup=popup,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"{row['city']} (AQI: {row.get('aqi', 'N/A')})"
        ).add_to(m)
        
    # Render map in Streamlit
    # width=800 is a good default, it will scale in columns
    st_folium(m, width="100%", height=500, returned_objects=[])
