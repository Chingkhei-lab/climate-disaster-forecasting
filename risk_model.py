def assess_risk(weather_data):
    """
    Analyzes weather data and returns a risk level.
    """
    if not weather_data or 'current' not in weather_data:
        return "No Data", "gray", "Unable to fetch local weather."

    # Extract Current Data safely
    current = weather_data.get('current', {})
    temp = current.get('temperature_2m', 0)
    rain = current.get('rain', 0)
    wind = current.get('wind_speed_10m', 0)
    soil = current.get('soil_moisture_0_to_1cm', 0)
    snow = current.get('snowfall', 0)
    
    # Extract Future Data safely
    daily = weather_data.get('daily', {})
    # Use [0.0] as default to prevent max() error on empty sequence
    precip_list = daily.get('precipitation_sum', [0.0])
    if not precip_list: precip_list = [0.0] 
    
    max_future_rain = max(precip_list)

    # --- RISK LOGIC ---
    
    # 1. CYCLONE
    if wind > 89:
        return "SEVERE CYCLONE", "red", f"Dangerous wind speeds of {wind} km/h detected."
    elif wind > 62:
        return "CYCLONE WARNING", "orange", f"High winds of {wind} km/h. Structural risk present."

    # 2. FLOOD
    if max_future_rain > 100:
        return "FLOOD FORECAST", "red", f"AI predicts {max_future_rain}mm rain in next 24h."
    elif rain > 50 and soil > 0.4:
        return "FLASH FLOOD RISK", "red", f"Heavy rain ({rain}mm) on saturated soil. Flooding imminent."
    elif rain > 20:
        return "HEAVY RAINFALL", "orange", f"Current rainfall: {rain} mm."

    # 3. HEATWAVE
    if temp > 45:
        return "EXTREME HEATWAVE", "red", f"Temperature is {temp}°C. Critical Danger."
    elif temp > 40:
        return "HEAT ALERT", "orange", f"Temperature is {temp}°C. Stay indoors."

    # 4. AVALANCHE
    if snow > 5:
        return "AVALANCHE RISK", "orange", f"Fresh snowfall of {snow} cm detected."

    return "Normal Conditions", "green", "No immediate meteorological threats detected."