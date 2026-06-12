def get_health_advisories(aqi):
    """
    Returns health advisories based on the AQI category.
    """
    if aqi <= 50:
        return {
            "general": "Air quality is considered satisfactory, and air pollution poses little or no risk.",
            "sensitive": "No precautions necessary.",
            "workers": "No precautions necessary.",
            "icon": "🟢"
        }
    elif aqi <= 100:
        return {
            "general": "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.",
            "sensitive": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
            "workers": "No precautions necessary.",
            "icon": "🟡"
        }
    elif aqi <= 200:
        return {
            "general": "Members of sensitive groups may experience health effects. The general public is not likely to be affected.",
            "sensitive": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
            "workers": "Consider limiting prolonged outdoor exertion.",
            "icon": "🟠"
        }
    elif aqi <= 300:
        return {
            "general": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.",
            "sensitive": "Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion.",
            "workers": "Reduce prolonged or heavy outdoor exertion.",
            "icon": "🔴"
        }
    elif aqi <= 400:
        return {
            "general": "Health warnings of emergency conditions. The entire population is more likely to be affected.",
            "sensitive": "Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion.",
            "workers": "Avoid all outdoor physical exertion.",
            "icon": "🟣"
        }
    else:
        return {
            "general": "Health alert: everyone may experience more serious health effects.",
            "sensitive": "Everyone should avoid all outdoor exertion.",
            "workers": "Avoid all outdoor physical exertion.",
            "icon": "🟤"
        }
