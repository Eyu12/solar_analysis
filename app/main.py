import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os

# ═══════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════
st.set_page_config(
    page_title="🌍 Worldwide Solar Intelligence",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #FF6B35, #F7C59F);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stSelectbox label {font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# NASA API FUNCTION
# ═══════════════════════════════════════
@st.cache_data(ttl=3600)
def fetch_solar_data(lat, lon, start, end, country_name):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,T2M,RH2M,WS2M,PRECTOTCORR",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            properties = data["properties"]["parameter"]
            df = pd.DataFrame(properties)
            df.index = pd.to_datetime(df.index, format="%Y%m%d")
            df["country"] = country_name
            return df
    except Exception as e:
        st.error(f"API Error: {e}")
    return None

# ═══════════════════════════════════════
# COUNTRY DATABASE
# ═══════════════════════════════════════
COUNTRIES = {
    "🇪🇹 Ethiopia":     {"lat": 9.03,   "lon": 38.74,  "continent": "Africa"},
    "🇧🇯 Benin":        {"lat": 9.31,   "lon": 2.32,   "continent": "Africa"},
    "🇸🇱 Sierra Leone": {"lat": 8.46,   "lon": -11.77, "continent": "Africa"},
    "🇪🇬 Egypt":        {"lat": 26.82,  "lon": 30.80,  "continent": "Africa"},
    "🇿🇦 South Africa": {"lat": -30.56, "lon": 22.94,  "continent": "Africa"},
    "🇮🇳 India":        {"lat": 20.59,  "lon": 78.96,  "continent": "Asia"},
    "🇨🇳 China":        {"lat": 35.86,  "lon": 104.19, "continent": "Asia"},
    "🇸🇦 Saudi Arabia": {"lat": 23.89,  "lon": 45.08,  "continent": "Asia"},
    "🇦🇪 UAE":          {"lat": 23.42,  "lon": 53.85,  "continent": "Asia"},
    "🇩🇪 Germany":      {"lat": 51.16,  "lon": 10.45,  "continent": "Europe"},
    "🇪🇸 Spain":        {"lat": 40.46,  "lon": -3.74,  "continent": "Europe"},
    "🇺🇸 USA":          {"lat": 37.09,  "lon": -95.71, "continent": "Americas"},
    "🇧🇷 Brazil":       {"lat": -14.24, "lon": -51.93, "continent": "Americas"},
    "🇨🇱 Chile":        {"lat": -35.67, "lon": -71.54, "continent": "Americas"},
    "🇦🇺 Australia":    {"lat": -25.27, "lon": 133.77, "continent": "Oceania"},
}

# ═══════════════════════════════════════
# HEADER
# ═══════════════════════════════════════
st.markdown('<div class="main-header">☀️ Worldwide Solar Intelligence Platform</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time NASA POWER Data • 15 Countries • ML Powered</div>', 
            unsafe_allow_html=True)
st.markdown("---")

# ═══════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px;'>
        <span style='font-size:2rem;'>🚀</span>
        <p style='color:#FF6B35; font-weight:bold; margin:0;'>NASA POWER</p>
        <p style='color:#666; font-size:0.8rem;'>Data Source</p>
    </div>
""", unsafe_allow_html=True)
    st.markdown("### ⚙️ Dashboard Controls")
    
    selected_countries = st.multiselect(
        "🌍 Select Countries",
        options=list(COUNTRIES.keys()),
        default=["🇪🇹 Ethiopia", "🇪🇬 Egypt", "🇩🇪 Germany", "🇦🇺 Australia", "🇮🇳 India"]
    )
    
    year = st.selectbox("📅 Select Year", [2021, 2022, 2023], index=2)
    
    st.markdown("---")
    st.markdown("### 📊 About")
    st.info("Built with NASA POWER API\nBy Eyayaw Zewdu\nArba Minch University")

# ═══════════════════════════════════════
# FETCH DATA
# ═══════════════════════════════════════
if not selected_countries:
    st.warning("⚠️ Please select at least one country from the sidebar!")
    st.stop()

with st.spinner("☀️ Fetching real NASA solar data..."):
    all_data = {}
    for country in selected_countries:
        info = COUNTRIES[country]
        clean_name = country.split(" ", 1)[1]
        df = fetch_solar_data(
            lat=info["lat"],
            lon=info["lon"],
            start=f"{year}0101",
            end=f"{year}1231",
            country_name=clean_name
        )
        if df is not None:
            all_data[clean_name] = df

# ═══════════════════════════════════════
# KPI METRICS
# ═══════════════════════════════════════
st.markdown("### 📈 Key Metrics")
cols = st.columns(len(all_data))
for idx, (country, df) in enumerate(all_data.items()):
    with cols[idx]:
        mean_val = df["ALLSKY_SFC_SW_DWN"].mean()
        max_val = df["ALLSKY_SFC_SW_DWN"].max()
        st.metric(
            label=f"☀️ {country}",
            value=f"{mean_val:.2f}",
            delta=f"Max: {max_val:.2f} kW-hr/m²/day"
        )

st.markdown("---")

# ═══════════════════════════════════════
# CHARTS
# ═══════════════════════════════════════
col1, col2 = st.columns(2)

# Chart 1 — Time Series
with col1:
    st.markdown("#### 📈 Solar Irradiance Over Time")
    fig1 = go.Figure()
    for country, df in all_data.items():
        fig1.add_trace(go.Scatter(
            x=df.index, y=df["ALLSKY_SFC_SW_DWN"],
            name=country, mode="lines", opacity=0.8
        ))
    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="kW-hr/m²/day",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2 — Bar Chart Ranking
with col2:
    st.markdown("#### 🏆 Country Solar Ranking")
    means = {c: df["ALLSKY_SFC_SW_DWN"].mean() 
             for c, df in all_data.items()}
    sorted_means = dict(sorted(means.items(), 
                               key=lambda x: x[1], reverse=True))
    fig2 = px.bar(
        x=list(sorted_means.values()),
        y=list(sorted_means.keys()),
        orientation="h",
        color=list(sorted_means.values()),
        color_continuous_scale="YlOrRd",
        labels={"x": "Mean kW-hr/m²/day", "y": "Country"}
    )
    fig2.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3 — Monthly Heatmap
st.markdown("#### 🌡️ Monthly Solar Heatmap")
monthly_data = {}
for country, df in all_data.items():
    monthly_data[country] = df["ALLSKY_SFC_SW_DWN"].resample("ME").mean().values[:12]

heatmap_df = pd.DataFrame(
    monthly_data,
    index=["Jan","Feb","Mar","Apr","May","Jun",
           "Jul","Aug","Sep","Oct","Nov","Dec"]
)
fig3 = px.imshow(
    heatmap_df,
    color_continuous_scale="YlOrRd",
    aspect="auto",
    text_auto=".1f"
)
fig3.update_layout(height=350)
st.plotly_chart(fig3, use_container_width=True)

# Chart 4 — Box Plot
st.markdown("#### 📦 Solar Distribution Comparison")
box_data = []
for country, df in all_data.items():
    for val in df["ALLSKY_SFC_SW_DWN"].values:
        box_data.append({"Country": country, "Solar": val})
box_df = pd.DataFrame(box_data)
fig4 = px.box(box_df, x="Country", y="Solar",
              color="Country",
              color_discrete_sequence=px.colors.qualitative.Set2)
fig4.update_layout(height=400, showlegend=False,
                   yaxis_title="kW-hr/m²/day")
st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════
# WORLD MAP
# ═══════════════════════════════════════
st.markdown("### 🗺️ World Solar Potential Map")

# Country coordinates and means
map_data = []
for country, df in all_data.items():
    # Find coordinates from COUNTRIES dict
    for key, info in COUNTRIES.items():
        if country in key:
            map_data.append({
                "country": country,
                "lat": info["lat"],
                "lon": info["lon"],
                "mean_solar": round(df["ALLSKY_SFC_SW_DWN"].mean(), 2),
                "max_solar": round(df["ALLSKY_SFC_SW_DWN"].max(), 2),
                "continent": info["continent"]
            })
            break

map_df = pd.DataFrame(map_data)

# Create world map
fig_map = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    color="mean_solar",
    size="mean_solar",
    hover_name="country",
    hover_data={
        "mean_solar": ":.2f",
        "max_solar": ":.2f",
        "continent": True,
        "lat": False,
        "lon": False
    },
    color_continuous_scale="YlOrRd",
    size_max=40,
    projection="natural earth",
    title="☀️ Solar Irradiance by Country (kW-hr/m²/day)"
)

fig_map.update_layout(
    height=500,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        showcountries=True,
        showland=True,
        showocean=True,
    ),
    margin=dict(l=0, r=0, t=40, b=0)
)


st.plotly_chart(fig_map, use_container_width=True)

# Top regions table
st.markdown("### 🏆 Top Solar Investment Regions")
top_regions = map_df.sort_values("mean_solar", ascending=False).reset_index(drop=True)
top_regions.index += 1
top_regions.columns = ["Country", "Latitude", "Longitude", 
                        "Mean Solar", "Max Solar", "Continent"]
top_regions = top_regions[["Country", "Continent", "Mean Solar", "Max Solar"]]

# Add medal emojis
medals = ["🥇", "🥈", "🥉"] + ["🏅"] * (len(top_regions) - 3)
top_regions.insert(0, "Rank", medals[:len(top_regions)])

st.dataframe(
    top_regions,
    use_container_width=True,
    hide_index=True
)

# ═══════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#666; font-size:0.9rem'>
    🌍 Worldwide Solar Intelligence Platform | 
    Built by Eyayaw Zewdu | 
    Arba Minch University | 
    Data: NASA POWER API
</div>
""", unsafe_allow_html=True)
