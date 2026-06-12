def explain_aqi(row, month):
    """
    row: dict with keys pm25, pm10, no2, co, aqi
    month: integer 1-12
    """
    reasons = []
    recommendations = []

    # Identify dominant pollutant
    pollutants = {"PM2.5": row.get("pm25", 0), "PM10": row.get("pm10", 0), "NO2": row.get("no2", 0)}
    dominant = max(pollutants, key=pollutants.get)
    dominant_val = pollutants[dominant]

    reasons.append(f"**{dominant}** is the primary contributor to today's AQI at {dominant_val:.1f} µg/m³.")

    # Seasonal context
    if month in [10, 11, 12, 1]:
        reasons.append("Winter months typically worsen AQI due to temperature inversions trapping pollutants near ground level.")
    elif month in [4, 5, 6]:
        reasons.append("Pre-monsoon dry conditions increase dust and PM10 levels.")
    elif month in [7, 8, 9]:
        reasons.append("Monsoon season usually improves AQI — elevated readings may indicate local industrial activity.")

    # PM2.5 specific
    if row.get("pm25", 0) > 60:
        reasons.append("High PM2.5 often indicates vehicle exhaust, industrial emissions, or crop burning nearby.")

    # PM10 specific
    if row.get("pm10", 0) > 100:
        reasons.append("Elevated PM10 suggests construction dust or wind-blown soil particles.")

    # NO2 specific
    if row.get("no2", 0) > 40:
        reasons.append("NO2 spike likely from heavy traffic or diesel vehicles in the area.")

    # Recommendations
    aqi = row.get("aqi", 0)
    if aqi > 200:
        recommendations = [
            "Avoid all outdoor activities.",
            "Keep windows and doors closed.",
            "Use an air purifier indoors if available.",
            "N95 mask mandatory if going outside."
        ]
    elif aqi > 150:
        recommendations = [
            "Sensitive groups (children, elderly, asthma patients) should stay indoors.",
            "Limit outdoor exercise.",
            "Wear a mask outdoors."
        ]
    elif aqi > 100:
        recommendations = [
            "Reduce prolonged outdoor exertion.",
            "Monitor symptoms if you have respiratory conditions."
        ]
    else:
        recommendations = ["Air quality is acceptable. Enjoy outdoor activities with normal precautions."]

    return reasons, recommendations
