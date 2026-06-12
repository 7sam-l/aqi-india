def calculate_sub_index(c, breakpoints):
    """
    Calculate the sub-index for a given pollutant concentration.
    breakpoints is a list of tuples: (BP_LO, BP_HI, I_LO, I_HI)
    """
    if c is None or c < 0:
        return 0

    for (bp_lo, bp_hi, i_lo, i_hi) in breakpoints:
        if bp_lo <= c <= bp_hi:
            return round(((i_hi - i_lo) / (bp_hi - bp_lo)) * (c - bp_lo) + i_lo)
    
    # If concentration exceeds highest breakpoint, extrapolate from the last interval
    last_bp = breakpoints[-1]
    bp_lo, bp_hi, i_lo, i_hi = last_bp
    return round(((i_hi - i_lo) / (bp_hi - bp_lo)) * (c - bp_lo) + i_lo)

def get_aqi_from_pollutants(pm25=None, pm10=None, no2=None, co=None, so2=None, o3=None):
    """
    Calculate overall AQI based on CPCB formula.
    Returns the maximum sub-index as the final AQI.
    """
    # Breakpoints format: (BP_LO, BP_HI, I_LO, I_HI)
    bp_pm25 = [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500)
    ]
    
    # Standard Indian CPCB breakpoints for other pollutants (approximate for the app)
    bp_pm10 = [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, 1000, 401, 500)
    ]
    
    bp_no2 = [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 1000, 401, 500)
    ]
    
    sub_indices = []
    
    if pm25 is not None:
        sub_indices.append(calculate_sub_index(pm25, bp_pm25))
    if pm10 is not None:
        sub_indices.append(calculate_sub_index(pm10, bp_pm10))
    if no2 is not None:
        sub_indices.append(calculate_sub_index(no2, bp_no2))
        
    if not sub_indices:
        return 0
        
    return max(sub_indices)

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Satisfactory", "yellow"
    elif aqi <= 200:
        return "Moderate", "orange"
    elif aqi <= 300:
        return "Poor", "red"
    elif aqi <= 400:
        return "Very Poor", "purple"
    else:
        return "Severe", "maroon"
