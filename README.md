# 📈 Capital Asset Pricing Model (CAPM) Web Application
An interactive financial analytics dashboard built with **Python**, **Streamlit**, and **Plotly** that tracks, cleans, and visualizes equity performance relative to the market benchmark (S&P 500). 
---
## 🚀 Project Overview
Analyzing historical stock data side-by-side with market indexes often involves tackling inconsistent date formats, timezone anomalies, and clumsy API responses. This application solves those issues by offering a seamless data pipeline that fetches live macroeconomic indicators and pairs them beautifully with continuous stock history—all inside a highly responsive user interface.

### Key Highlights
* **Dual-Stream Data Harvesting:** Pulls live pricing structures from Yahoo Finance while simultaneously hitting the Federal Reserve Economic Data (**FRED**) database for reliable S&P 500 records.
* **Deterministic Data Preprocessing:** Programmatically resolves nested MultiIndex frames and normalizes temporal properties across mismatched streams.
* **Vectorized Data Graphics:** Leverages low-level Plotly structures for quick rendering times and an uncluttered user layout.
---
## 🛠️ Tech Stack & Ecosystem
| Component | Library / Framework | Primary Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | `Streamlit` | Multi-column layout, client configuration state management. |
| **Visualization** | `Plotly (Graph Objects)` | Interactive multi-line continuous time-series plotting. |
| **Data Scraping** | `yfinance` & `pandas_datareader` | Live equity pricing inputs and FRED benchmark harvesting. |
| **Wrangling Engine** | `Pandas` | Structural manipulation, inner joins, and timezone stripping. |
---
## ⚙️ Data Pipeline Architecture
Raw financial telemetry is volatile and often prone to breaks. The underlying core of this codebase functions around a dedicated cleanup workflow:

1. **MultiIndex Flattening:** Newer versions of commercial stock APIs bundle single variables inside structured tuple matrices. The core controller checks for `isinstance(data.columns, pd.MultiIndex)` and instantly strips the outer layers to prevent `ValueError` key exceptions.
2. **Timezone Normalization:** S&P 500 index indicators from FRED arrive as naive timestamps, while standard equity brokers supply localized UTC timestamps. The pipeline flattens this gap instantly via `.dt.tz_localize(None)` to achieve an exact **inner join**.
3. **Data Previews:** Generates isolated `head()` and `tail()` snapshots inside independent UI columns to allow rapid analytical review without screen space clutter.
---
## 📂 Repository Structure
```text
├── capm_functions.py  # Graphic engine handling custom Plotly configurations
├── CAPM_Return.py       # Main controller orchestrating data pipelines & UI state
├── requirements.txt  # Project ecosystem dependency registry
├── Calculate_Beta.py #Returns the beta value of each stocks
└── .gitignore        # Keeps build footprints and local caches out of source control
