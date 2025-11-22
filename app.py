import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import data_manager as dm
import risk_model as rm
import ai_agent as ai

# --- PAGE CONFIG ---
st.set_page_config(page_title="DisasterGuard AI", layout="wide", page_icon="🛡️")

# --- HEADER ---
st.title("🛡️ AI Climate Disaster Forecasting")
st.markdown("Powered by **ECMWF (Weather)** and **DeepSeek R1 (AI Strategy)**")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛰️ Data Layers")
    show_fires = st.checkbox("🔥 NASA Active Fires", value=True)
    show_alerts = st.checkbox("⚠️ GDACS Global Alerts", value=True)
    st.divider()
    st.caption("System Status: **ONLINE** 🟢")

# --- MAP INITIALIZATION ---
m = folium.Map(location=[21.1458, 79.0882], zoom_start=5, tiles="CartoDB positron")

if show_fires:
    fires = dm.fetch_nasa_fire_data()
    if not fires.empty:
        for _, row in fires.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=2, color="#ff4b4b", fill=True, fill_opacity=0.6,
                tooltip=f"🔥 Fire (Conf: {row['confidence']}%)"
            ).add_to(m)

if show_alerts:
    alerts = dm.fetch_gdacs_alerts()
    if not alerts.empty:
        for _, row in alerts.iterrows():
            icon_color = "purple" if "Cyclone" in row['title'] else "blue"
            folium.Marker(
                location=[row['lat'], row['lon']],
                icon=folium.Icon(color=icon_color, icon="exclamation-triangle", prefix="fa"),
                tooltip=f"⚠️ {row['title']}"
            ).add_to(m)

m.add_child(folium.LatLngPopup())

# --- LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    map_data = st_folium(m, height=650, width=None)

with col2:
    st.subheader("📡 Intelligence Terminal")
    
    if map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]
        
        st.info(f"Target Locked: **{lat:.4f}, {lng:.4f}**")
        
        with st.spinner(" establishing Satellite Uplink..."):
            weather = dm.fetch_weather(lat, lng)
        
        if weather:
            # 1. LOGIC MODEL
            status, color, msg = rm.assess_risk(weather)
            
            # 2. AI AGENT (DeepSeek)
            with st.spinner("🤖 DeepSeek R1 is analyzing strategy..."):
                ai_report = ai.generate_disaster_report(lat, lng, weather, status)

            # --- DISPLAY UI ---
            if color == "red": 
                st.error(f"### 🚨 {status}")
            elif color == "orange": 
                st.warning(f"### ⚠️ {status}")
            else: 
                st.success(f"### ✅ {status}")
            
            st.caption(msg)
            
            with st.expander("📄 Read Strategic Briefing", expanded=True):
                st.markdown(ai_report)

            # 3. METRICS
            curr = weather.get('current', {})
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Temp", f"{curr.get('temperature_2m', 0)}°C")
            c2.metric("Wind", f"{curr.get('wind_speed_10m', 0)} km/h")
            c3.metric("Rain", f"{curr.get('rain', 0)} mm")

            # 4. CHARTS
            daily = weather.get('daily', {})
            if daily:
                st.subheader("📅 7-Day Forecast")
                df_chart = pd.DataFrame({
                    "Date": daily.get('time',),
                    "Max Temp (°C)": daily.get('temperature_2m_max',),
                    "Precipitation (mm)": daily.get('precipitation_sum',)
                })
                st.line_chart(df_chart, x="Date", y="Max Temp (°C)", color="#FF4B4B")
                st.bar_chart(df_chart, x="Date", y="Precipitation (mm)", color="#0083B8")
        else:
            st.error("❌ Connection Lost")
            st.warning("Unable to fetch weather data.")
            
    else:
        st.info("👈 Click anywhere on the map to initiate analysis.")