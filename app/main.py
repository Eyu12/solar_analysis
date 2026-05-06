import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests

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
    .stSelectbox label {font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════
MONTH_NAMES     = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
NASA_MONTH_KEYS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                   "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

COUNTRIES = {
    "🇪🇹 Ethiopia":     {"lat":  9.03,  "lon":  38.74, "continent": "Africa"},
    "🇧🇯 Benin":        {"lat":  9.31,  "lon":   2.32, "continent": "Africa"},
    "🇸🇱 Sierra Leone": {"lat":  8.46,  "lon": -11.77, "continent": "Africa"},
    "🇪🇬 Egypt":        {"lat": 26.82,  "lon":  30.80, "continent": "Africa"},
    "🇿🇦 South Africa": {"lat":-30.56,  "lon":  22.94, "continent": "Africa"},
    "🇮🇳 India":        {"lat": 20.59,  "lon":  78.96, "continent": "Asia"},
    "🇨🇳 China":        {"lat": 35.86,  "lon": 104.19, "continent": "Asia"},
    "🇸🇦 Saudi Arabia": {"lat": 23.89,  "lon":  45.08, "continent": "Asia"},
    "🇦🇪 UAE":          {"lat": 23.42,  "lon":  53.85, "continent": "Asia"},
    "🇩🇪 Germany":      {"lat": 51.16,  "lon":  10.45, "continent": "Europe"},
    "🇪🇸 Spain":        {"lat": 40.46,  "lon":  -3.74, "continent": "Europe"},
    "🇺🇸 USA":          {"lat": 37.09,  "lon": -95.71, "continent": "Americas"},
    "🇧🇷 Brazil":       {"lat":-14.24,  "lon": -51.93, "continent": "Americas"},
    "🇨🇱 Chile":        {"lat":-35.67,  "lon": -71.54, "continent": "Americas"},
    "🇦🇺 Australia":    {"lat":-25.27,  "lon": 133.77, "continent": "Oceania"},
}

# ═══════════════════════════════════════
# HELPER
# ═══════════════════════════════════════
def get_month_value(param_dict, month_int):
    """Get monthly value using NASA uppercase month keys e.g. JAN, FEB"""
    key = NASA_MONTH_KEYS[month_int - 1]
    val = param_dict.get(key, 0)
    return float(val) if val and float(val) > -900 else 0.0

# ═══════════════════════════════════════
# API FUNCTIONS
# ═══════════════════════════════════════
@st.cache_data(ttl=3600)
def fetch_solar_data(lat, lon, start, end, country_name):
    """Fetch daily solar data from NASA POWER API"""
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


@st.cache_data(ttl=3600)
def fetch_climatology_data(lat, lon):
    """Fetch long-term climatology data from NASA POWER API"""
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,T2M,RH2M,WS2M",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data["properties"]["parameter"]
    except Exception as e:
        st.error(f"Climatology API Error: {e}")
    return None

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
# FETCH DAILY DATA
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
            lat=info["lat"], lon=info["lon"],
            start=f"{year}0101", end=f"{year}1231",
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
        max_val  = df["ALLSKY_SFC_SW_DWN"].max()
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

with col1:
    st.markdown("#### 📈 Solar Irradiance Over Time")
    fig1 = go.Figure()
    for country, df in all_data.items():
        fig1.add_trace(go.Scatter(
            x=df.index, y=df["ALLSKY_SFC_SW_DWN"],
            name=country, mode="lines", opacity=0.8
        ))
    fig1.update_layout(
        xaxis_title="Date", yaxis_title="kW-hr/m²/day", height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 🏆 Country Solar Ranking")
    means = {c: df["ALLSKY_SFC_SW_DWN"].mean() for c, df in all_data.items()}
    sorted_means = dict(sorted(means.items(), key=lambda x: x[1], reverse=True))
    fig2 = px.bar(
        x=list(sorted_means.values()), y=list(sorted_means.keys()),
        orientation="h", color=list(sorted_means.values()),
        color_continuous_scale="YlOrRd",
        labels={"x": "Mean kW-hr/m²/day", "y": "Country"}
    )
    fig2.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### 🌡️ Monthly Solar Heatmap")
monthly_data = {}
for country, df in all_data.items():
    monthly_data[country] = df["ALLSKY_SFC_SW_DWN"].resample("ME").mean().values[:12]
heatmap_df = pd.DataFrame(monthly_data, index=MONTH_NAMES)
fig3 = px.imshow(heatmap_df, color_continuous_scale="YlOrRd", aspect="auto", text_auto=".1f")
fig3.update_layout(height=350)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("#### 📦 Solar Distribution Comparison")
box_data = []
for country, df in all_data.items():
    for val in df["ALLSKY_SFC_SW_DWN"].values:
        box_data.append({"Country": country, "Solar": val})
box_df = pd.DataFrame(box_data)
fig4 = px.box(box_df, x="Country", y="Solar", color="Country",
              color_discrete_sequence=px.colors.qualitative.Set2)
fig4.update_layout(height=400, showlegend=False, yaxis_title="kW-hr/m²/day")
st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════
# WORLD MAP
# ═══════════════════════════════════════
st.markdown("### 🗺️ World Solar Potential Map")

map_data = []
for country, df in all_data.items():
    for key, info in COUNTRIES.items():
        if country in key:
            map_data.append({
                "country":    country,
                "lat":        info["lat"],
                "lon":        info["lon"],
                "mean_solar": round(df["ALLSKY_SFC_SW_DWN"].mean(), 2),
                "max_solar":  round(df["ALLSKY_SFC_SW_DWN"].max(), 2),
                "continent":  info["continent"]
            })
            break

map_df = pd.DataFrame(map_data)
fig_map = px.scatter_geo(
    map_df, lat="lat", lon="lon",
    color="mean_solar", size="mean_solar",
    hover_name="country",
    hover_data={"mean_solar": ":.2f", "max_solar": ":.2f",
                "continent": True, "lat": False, "lon": False},
    color_continuous_scale="YlOrRd", size_max=40,
    projection="natural earth",
    title="☀️ Solar Irradiance by Country (kW-hr/m²/day)"
)
fig_map.update_layout(
    height=500,
    geo=dict(showframe=False, showcoastlines=True,
             showcountries=True, showland=True, showocean=True),
    margin=dict(l=0, r=0, t=40, b=0)
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("### 🏆 Top Solar Investment Regions")
top_regions = map_df.sort_values("mean_solar", ascending=False).reset_index(drop=True)
top_regions.columns = ["Country", "Latitude", "Longitude", "Mean Solar", "Max Solar", "Continent"]
top_regions = top_regions[["Country", "Continent", "Mean Solar", "Max Solar"]]
medals = ["🥇", "🥈", "🥉"] + ["🏅"] * (len(top_regions) - 3)
top_regions.insert(0, "Rank", medals[:len(top_regions)])
st.dataframe(top_regions, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════
# SOLAR PREDICTION TOOL
# ═══════════════════════════════════════
st.markdown("---")
st.markdown("### 🔮 Solar Prediction Tool")
st.markdown("*Enter any location to get real NASA solar data and investment rating!*")

col1, col2 = st.columns(2)

with col1:
    pred_lat = st.number_input(
        "📍 Latitude", min_value=-90.0, max_value=90.0,
        value=6.03, help="Range: -90 to 90"
    )
    pred_lon = st.number_input(
        "📍 Longitude", min_value=-180.0, max_value=180.0,
        value=37.55, help="Range: -180 to 180"
    )

with col2:
    pred_month = st.selectbox(
        "📅 Select Month",
        options=list(range(1, 13)),
        format_func=lambda x: MONTH_NAMES[x - 1],
        index=5
    )
    st.markdown("""
    <div style='background:#1a1a2e; padding:10px; border-radius:8px; margin-top:8px;'>
        <p style='color:#FF6B35; margin:0; font-size:0.85rem;'>📌 Quick Reference</p>
        <p style='color:#aaa; margin:0; font-size:0.8rem;'>🇪🇹 Arba Minch: 6.03, 37.55</p>
        <p style='color:#aaa; margin:0; font-size:0.8rem;'>🇪🇹 Debre Tabor: 11.85, 38.01</p>
        <p style='color:#aaa; margin:0; font-size:0.8rem;'>🇱🇧 Beirut: 33.89, 35.50</p>
        <p style='color:#aaa; margin:0; font-size:0.8rem;'>🇬🇷 Athens: 37.98, 23.73</p>
        <p style='color:#aaa; margin:0; font-size:0.8rem;'>🇬🇧 London: 51.51, -0.13</p>
        <p style='color:#aaa; margin:0; font-size:0.8rem;'>🇳🇴 Oslo: 59.91, 10.75</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("⚡ Get Solar Data & Prediction!", type="primary", use_container_width=True):

    with st.spinner(f"🌐 Fetching real NASA data for ({pred_lat}, {pred_lon})..."):
        clim_data = fetch_climatology_data(pred_lat, pred_lon)

    if clim_data:
        # Extract monthly values using correct NASA uppercase keys
        solar    = get_month_value(clim_data["ALLSKY_SFC_SW_DWN"], pred_month)
        clrsky   = get_month_value(clim_data["CLRSKY_SFC_SW_DWN"], pred_month)
        temp     = get_month_value(clim_data["T2M"],               pred_month)
        humidity = get_month_value(clim_data["RH2M"],              pred_month)
        wind     = get_month_value(clim_data["WS2M"],              pred_month)

        # Annual average directly from NASA ANN key
        annual_avg = float(clim_data["ALLSKY_SFC_SW_DWN"].get("ANN", 0))
        if annual_avg <= 0:
            annual_avg = np.mean([
                get_month_value(clim_data["ALLSKY_SFC_SW_DWN"], m)
                for m in range(1, 13)
            ])

        # Rating
        if solar >= 6.5:
            rating = "🔥 Exceptional"
            color  = "#FF4500"
            advice = "World class solar potential — ideal for large scale solar farm!"
        elif solar >= 5.5:
            rating = "✅ Excellent"
            color  = "#FF6B35"
            advice = "Outstanding solar potential — highly recommended for investment!"
        elif solar >= 4.5:
            rating = "👍 Very Good"
            color  = "#1A936F"
            advice = "Great potential — suitable for solar installation!"
        elif solar >= 3.5:
            rating = "⚠️ Moderate"
            color  = "#004E89"
            advice = "Moderate potential — consider with backup energy sources."
        else:
            rating = "❌ Poor"
            color  = "#666"
            advice = "Low solar potential — not recommended for solar investment."

        # Season
        season = (
            "Summer ☀️" if pred_month in [6, 7, 8]  else
            "Winter ❄️" if pred_month in [12, 1, 2] else
            "Spring 🌸" if pred_month in [3, 4, 5]  else
            "Autumn 🍂"
        )

        # Result card
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}, #1a1a2e);
                    padding: 2rem; border-radius: 15px;
                    text-align: center; margin: 1rem 0;'>
            <h2 style='color:white; margin:0; font-size:2.5rem;'>
                {solar:.2f} kW-hr/m²/day
            </h2>
            <h3 style='color:white; margin:0.5rem 0;'>{rating}</h3>
            <p style='color:rgba(255,255,255,0.85); margin:0;'>{advice}</p>
            <p style='color:rgba(255,255,255,0.6); font-size:0.85rem; margin-top:0.8rem;'>
                📍 Lat: {pred_lat} | Lon: {pred_lon} |
                {MONTH_NAMES[pred_month-1]} | {season}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # NASA weather metrics
        st.markdown("#### 📡 Real NASA Climatology Data")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("☀️ Solar",     f"{solar:.2f}",    "kW-hr/m²/day")
        c2.metric("🌤️ Clear Sky", f"{clrsky:.2f}",   "kW-hr/m²/day")
        c3.metric("🌡️ Temp",      f"{temp:.1f}",     "°C")
        c4.metric("💧 Humidity",  f"{humidity:.1f}", "%")
        c5.metric("💨 Wind",      f"{wind:.1f}",     "m/s")

        # Monthly profile chart
        st.markdown("#### 📊 Monthly Solar Profile for This Location")
        monthly_solar = []
        for m in range(1, 13):
            val = get_month_value(clim_data["ALLSKY_SFC_SW_DWN"], m)
            monthly_solar.append({
                "Month":    MONTH_NAMES[m - 1],
                "Solar":    val,
                "Selected": "Selected" if m == pred_month else "Other"
            })

        monthly_df = pd.DataFrame(monthly_solar)
        fig_monthly = px.bar(
            monthly_df, x="Month", y="Solar",
            color="Selected",
            color_discrete_map={"Selected": "#FF6B35", "Other": "#444"},
            labels={"Solar": "kW-hr/m²/day"}
        )
        fig_monthly.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_monthly, use_container_width=True)

        # Annual summary
        st.markdown(f"""
        <div style='background:#1a1a2e; padding:1rem;
                    border-radius:10px; text-align:center;'>
            <p style='color:#FF6B35; font-weight:bold; margin:0;'>
                📅 Annual Average Solar Irradiance: {annual_avg:.2f} kW-hr/m²/day
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("❌ Could not fetch NASA data. Please check coordinates and try again!")

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
