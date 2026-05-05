import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
import joblib

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
# API FUNCTIONS
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


@st.cache_data(ttl=3600)
def fetch_prediction_data(lat, lon, month):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,T2M,RH2M,WS2M,PRECTOTCORR",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            props = data["properties"]["parameter"]
            month_str = str(month).zfill(2)
            return {
                "ALLSKY": props["ALLSKY_SFC_SW_DWN"].get(month_str, 5.5),
                "CLRSKY": props["CLRSKY_SFC_SW_DWN"].get(month_str, 7.5),
                "T2M": props["T2M"].get(month_str, 25.0),
                "RH2M": props["RH2M"].get(month_str, 45.0),
                "WS2M": props["WS2M"].get(month_str, 3.0),
            }
    except:
        pass
    return None


@st.cache_resource
def load_model():
    try:
        model = joblib.load("scripts/solar_model.pkl")
        le_c = joblib.load("scripts/le_country.pkl")
        le_s = joblib.load("scripts/le_season.pkl")
        return model, le_c, le_s
    except:
        return None, None, None

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
    means = {c: df["ALLSKY_SFC_SW_DWN"].mean() for c, df in all_data.items()}
    sorted_means = dict(sorted(means.items(), key=lambda x: x[1], reverse=True))
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
    index=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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
fig4 = px.box(
    box_df, x="Country", y="Solar",
    color="Country",
    color_discrete_sequence=px.colors.qualitative.Set2
)
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
                "country": country,
                "lat": info["lat"],
                "lon": info["lon"],
                "mean_solar": round(df["ALLSKY_SFC_SW_DWN"].mean(), 2),
                "max_solar": round(df["ALLSKY_SFC_SW_DWN"].max(), 2),
                "continent": info["continent"]
            })
            break

map_df = pd.DataFrame(map_data)

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
top_regions.columns = ["Country", "Latitude", "Longitude", "Mean Solar", "Max Solar", "Continent"]
top_regions = top_regions[["Country", "Continent", "Mean Solar", "Max Solar"]]
medals = ["🥇", "🥈", "🥉"] + ["🏅"] * (len(top_regions) - 3)
top_regions.insert(0, "Rank", medals[:len(top_regions)])
st.dataframe(top_regions, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════
# SOLAR PREDICTION TOOL
# ═══════════════════════════════════════
st.markdown("### 🔮 Solar Prediction Tool")
st.markdown("*Enter any location to predict solar irradiance using real NASA data!*")

model, le_c, le_s = load_model()

if model is None:
    st.warning("⚠️ Model not found! Please train and save the model first.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        pred_lat = st.number_input(
            "📍 Latitude", min_value=-90.0, max_value=90.0,
            value=9.03, help="Ethiopia = 9.03"
        )
        pred_lon = st.number_input(
            "📍 Longitude", min_value=-180.0, max_value=180.0,
            value=38.74, help="Ethiopia = 38.74"
        )

    with col2:
        pred_month = st.slider("📅 Month", 1, 12, 6, format="%d")
        pred_temp = st.number_input(
            "🌡️ Temperature (°C)", min_value=-20.0, max_value=50.0, value=25.0
        )

    with col3:
        pred_humidity = st.number_input(
            "💧 Humidity (%)", min_value=0.0, max_value=100.0, value=45.0
        )
        pred_wind = st.number_input(
            "💨 Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=3.0
        )

    if st.button("⚡ Predict Solar Irradiance!", type="primary", use_container_width=True):

        # Determine season
        season = (
            "Summer" if pred_month in [6, 7, 8] else
            "Winter" if pred_month in [12, 1, 2] else
            "Spring" if pred_month in [3, 4, 5] else
            "Autumn"
        )

        known_seasons = list(le_s.classes_)
        if season not in known_seasons:
            season = known_seasons[0]
        season_enc = le_s.transform([season])[0]

        # Fetch real NASA climatology data
        with st.spinner("🌐 Fetching real NASA data for this location..."):
            nasa_data = fetch_prediction_data(pred_lat, pred_lon, pred_month)

        if nasa_data:
            solar_avg = nasa_data["ALLSKY"]
            clrsky = nasa_data["CLRSKY"]
            clear_ratio = solar_avg / clrsky if clrsky > 0 else 0.75
            real_temp = nasa_data["T2M"]
            real_humidity = nasa_data["RH2M"]
            real_wind = nasa_data["WS2M"]
        else:
            solar_avg = 5.5
            clrsky = 7.5
            clear_ratio = 0.75
            real_temp = pred_temp
            real_humidity = pred_humidity
            real_wind = pred_wind

        # Build feature vector with real data
        sample = pd.DataFrame([{
            "T2M": real_temp,
            "RH2M": real_humidity,
            "WS2M": real_wind,
            "PRECTOTCORR": 0.1,
            "month": pred_month,
            "day_of_year": pred_month * 30,
            "country_encoded": 0,
            "season_encoded": season_enc,
            "lat": pred_lat,
            "lon": pred_lon,
            "solar_7day_avg": solar_avg,
            "solar_30day_avg": solar_avg * 0.95,
            "CLRSKY_SFC_SW_DWN": clrsky,
            "clear_sky_ratio": clear_ratio
        }])

        prediction = model.predict(sample)[0]

        # Rating
        if prediction >= 6.0:
            rating = "🔥 Excellent"
            color = "#FF6B35"
            advice = "Perfect for large scale solar farm investment!"
        elif prediction >= 5.0:
            rating = "✅ Very Good"
            color = "#F79B35"
            advice = "Great potential for solar installation!"
        elif prediction >= 4.0:
            rating = "👍 Good"
            color = "#1A936F"
            advice = "Suitable for solar energy projects!"
        elif prediction >= 3.0:
            rating = "⚠️ Moderate"
            color = "#004E89"
            advice = "Consider solar with backup energy sources."
        else:
            rating = "❌ Poor"
            color = "#666"
            advice = "Not recommended for solar investment."

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}, #333);
                    padding: 2rem; border-radius: 15px;
                    text-align: center; margin-top: 1rem;'>
            <h2 style='color: white; margin:0;'>{prediction:.2f} kW-hr/m²/day</h2>
            <h3 style='color: white; margin:0.5rem 0;'>{rating}</h3>
            <p style='color: rgba(255,255,255,0.8); margin:0;'>{advice}</p>
            <p style='color: rgba(255,255,255,0.6); font-size:0.8rem; margin-top:0.5rem;'>
                📍 Lat: {pred_lat} | Lon: {pred_lon} |
                Month: {pred_month} | Season: {season}
            </p>
        </div>
        """, unsafe_allow_html=True)

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