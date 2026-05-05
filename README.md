# ☀️ Worldwide Solar Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)
![NASA](https://img.shields.io/badge/Data-NASA%20POWER-green)
![ML](https://img.shields.io/badge/ML-XGBoost%2099.8%25-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A real-time worldwide solar intelligence platform powered by NASA POWER API 
> and Machine Learning — analyzing solar potential across 15 countries and 5 continents.

🔗 **Live Demo:** https://solaranalysis-4auwlndqrj7zyk9k64wrem.streamlit.app/

---

## 🌍 Overview

This project analyzes and predicts solar irradiance across 15 countries worldwide 
using real-time NASA POWER API data. It provides actionable insights for solar 
energy investment decisions through interactive visualizations and a 
high-accuracy machine learning model.

Built as part of the **SAFEE KAIM — Kifiya AI Mastery Training Program** 
(Mastercard Foundation & 10 Academy), this project extends the original 
3-country analysis into a comprehensive worldwide solar intelligence platform.

---

## ✨ Features

- 🌐 **Real-time NASA Data** — Live solar data from NASA POWER API
- 🌍 **15 Countries** across 5 continents
- 📊 **Interactive Dashboard** — Built with Streamlit and Plotly
- 🤖 **ML Prediction Model** — XGBoost with 99.8% accuracy (R²=0.9985)
- 📈 **4 Visualization Types** — Time series, ranking, heatmap, distribution
- 🏆 **Country & Continent Ranking** — Identify best solar investment regions
- ☀️ **Key Finding** — Ethiopia ranks Top 5 worldwide in solar potential!

---

## 🗺️ Countries Analyzed

| Continent | Countries |
|---|---|
| 🌍 Africa | Ethiopia, Egypt, Benin, Sierra Leone, South Africa |
| 🌏 Asia | India, China, Saudi Arabia, UAE |
| 🌍 Europe | Germany, Spain |
| 🌎 Americas | USA, Brazil, Chile |
| 🌏 Oceania | Australia |

---

## 🤖 Machine Learning Model

| Metric | Value |
|---|---|
| Algorithm | XGBoost Regressor |
| R² Score | 0.9985 |
| Accuracy | 99.8% |
| MAE | 0.0512 kW-hr/m²/day |
| Features | 14 engineered features |

### Top Features
1. 🥇 Solar 7-day rolling average
2. 🥈 Clear sky ratio
3. 🥉 Clear sky irradiance (CLRSKY)
4. 🌍 Geographic coordinates
5. 📅 Day of year & month

---

## 🏆 Key Findings

- 🥇 **Oceania** is the highest solar continent (6.31 kW-hr/m²/day)
- 🥈 **Africa** is the most consistent continent for solar energy
- 🇪🇹 **Ethiopia** ranks **Top 5 worldwide** — highest non-desert country!
- 🇪🇬 **Egypt** leads all countries (Sahara Desert advantage)
- 🇩🇪 **Germany** has the most seasonal variability
- 🌍 **Africa** is the best continent for long-term solar investment

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/worldwide-solar-intelligence.git

# Navigate to project
cd worldwide-solar-intelligence

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
cd app
streamlit run main.py
```

---

## 📁 Project Structure

worldwide-solar-intelligence/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── init.py
│   └── main.py          # Streamlit dashboard
├── notebooks/
│   ├── 01_nasa_api_exploration.ipynb
│   └── compare_countries.ipynb
├── scripts/
│   └── init.py
├── tests/
│   └── init.py
├── data/                # gitignored
├── requirements.txt
└── README.md

---

## 📊 Dashboard Preview

### Key Metrics
- Real-time solar irradiance per country
- Interactive country selector
- Year selector (2021-2023)

### Visualizations
- 📈 Solar irradiance over time
- 🏆 Country solar ranking
- 🌡️ Monthly solar heatmap
- 📦 Distribution comparison

---

## 🔬 Data Source

- **NASA POWER API** — https://power.larc.nasa.gov/
- Parameters: GHI, Clear Sky Irradiance, Temperature, Humidity, Wind Speed, Precipitation
- Temporal Resolution: Daily
- Coverage: 2021-2023

---

## 👨‍💻 Author

**Eyayaw Zewdu Ejigu**
- 📡 MSc Communication Engineering
- 🎓 Lecturer — Arba Minch University, Ethiopia
- 💻 MSIT Student — Florida University
- 🏆 KAIM Certified — Kifiya AI Mastery Program (with Distinction)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- **NASA POWER** for providing free worldwide solar data
- **10 Academy** and **Kifiya Financial Technology** for the KAIM program
- **Mastercard Foundation** for supporting AI education in Africa
- **Arba Minch University** for the research environment

---

<div align="center">
⭐ If you find this project useful, please give it a star on GitHub! ⭐

Built with ❤️ from Ethiopia 🇪🇹
</div>