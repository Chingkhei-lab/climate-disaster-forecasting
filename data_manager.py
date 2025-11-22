import requests
import pandas as pd
import xmltodict
import streamlit as st

# --- 1. WEATHER DATA (Open-Meteo Auto-Select) ---
@st.cache_data(ttl=300)
def fetch_weather(lat, lon):
    """
    Fetches weather data using the 'Best Match' model.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m", "soil_moisture_0_to_1cm", "snowfall"],
            "daily": ["temperature_2m_max", "precipitation_sum"],
            "timezone": "auto"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code!= 200:
            return None
            
        return response.json()
    except Exception:
        return None

# --- 2. FIRE DATA (NASA FIRMS) ---
@st.cache_data(ttl=3600)
def fetch_nasa_fire_data():
    url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_Asia_24h.csv"
    try:
        df = pd.read_csv(url)
        return df[df['confidence'] > 70]
    except Exception:
        return pd.DataFrame()

# --- 3. GLOBAL DISASTER ALERTS (GDACS) ---
@st.cache_data(ttl=3600)
def fetch_gdacs_alerts():
    url = "https://www.gdacs.org/xml/rss.xml"
    try:
        response = requests.get(url, timeout=10)
        data = xmltodict.parse(response.content)
        
        # Safe access to nested keys
        rss = data.get('rss', {})
        channel = rss.get('channel', {})
        items = channel.get('item',)
        
        # Handle case where there is only one item (dict instead of list)
        if isinstance(items, dict):
            items = [items]
            
        alerts = "" # <--- FIXED: Added brackets to initialize empty list
        
        for item in items:
            point = item.get('georss:point')
            if not point: continue
            
            try:
                lat, lon = map(float, point.split())
                alerts.append({
                    'title': item.get('title', 'Unknown Event'),
                    'description': item.get('description', ''),
                    'lat': lat,
                    'lon': lon,
                    'type': item.get('gdacs:eventtype', 'Unknown')
                })
            except:
                continue
        return pd.DataFrame(alerts)
    except Exception:
        return pd.DataFrame()