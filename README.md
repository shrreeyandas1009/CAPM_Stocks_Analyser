# 📈 Capital Asset Pricing Model (CAPM) Web Suite
An interactive, multi-page financial analytics suite built with **Streamlit** and **Plotly** designed to parse equity datasets, model asset volatility metrics (Beta), and project expected returns using the Capital Asset Pricing Model.
---
## 🚀 Live Application Architecture
The application is deployed live on Streamlit Community Cloud and features a dynamic multi-page workflow driven by user-state selection inputs:
### Page 1: 📊 CAPM Return (Core Dashboard)
* **Comparative Normalization:** Visualizes raw asset close prices side-by-side with an automatically normalized time-series chart starting from a common base ($1.0$).
* **Aggregated Portfolio Tracking:** Generates analytical summary matrices compiling calculated Beta metrics and expected asset returns synchronously across four selected equities.
### Page 2: 🎯 Calculate Beta (Individual Assessment)
* **Single-Asset Modeling:** Isolates a chosen stock asset to run variance-covariance analysis against the market index over a customizable 1–10 year timeline.
* **Ordinary Least Squares (OLS) Regression:** Automatically plots a dynamic Plotly scatter distribution mapping stock daily returns against market returns, featuring a crimson trendline tracking the asset's specific systemic risk profile ($\beta$).
---
## ⚙️ Financial & Data Data Pipeline
Raw market data varies significantly across broker architectures. This repository implements a robust data-cleaning mechanism to align tracking fields:

```text
  [yfinance Stock Tracker]             [FRED Federal Reserve API]
             │                                      │
             ▼                                      ▼
  [MultiIndex Header Clean]                         │
             │                                      │
             ▼                                      ▼
  [Timezone Stripping (Naive)] ──► Inner Join ◄── [DateTime Alignment]

```

1. **Header Hierarchies:** Evaluates structural layers using `isinstance(data.columns, pd.MultiIndex)` to flatten compound data matrices down to un-nested column groups, preventing downstream data assignment failures.
2. **Temporal Alignment:** Rectifies timezone mismatches between UTC financial data packages (`yfinance`) and timezone-naive economic indexes (`FRED`) via vectorized `.dt.tz_localize(None)` steps to safeguard strict inner joins.
3. **Daily Return Conversions:** Computes daily variance metrics using time-series delta conversions, establishing an annualized market expected return ($R_m$) used inside the CAPM formulation:

$$E(R_i) = R_f + \beta_i (E(R_m) - R_f)$$


---

## 📂 Repository File System

```text
├── CAPM_Return.py         # Home view & multi-asset comparative overview dashboard
├── capm_functions.py      # Statistical core engine (Beta calculations, OLS vectors)
├── requirements.txt       # Global dependency configuration manifest
├── .gitignore             # Suppresses runtime cache steps & system track files
└── pages/                 # Streamlit Multipage Core Directory
    └── Calculate_Beta.py  # Page 2 script: Single-stock variance regression workspace

```

---

## 🛠️ Local Installation & Environment Setup

To mirror this cloud deployment locally on your machine, initialize the following environment operations:

### 1. Clone the Source File Setup

```bash
git clone [https://github.com/shreeyandas1009/CAPM_Stocks_Analyser.git](https://github.com/shreeyandas1009/CAPM_Stocks_Analyser.git)
cd CAPM_Stocks_Analyser

```

### 2. Install Package Core Registry

Ensure your workspace includes Python 3.8+ before initializing library dependencies:

```bash
pip install -r requirements.txt

```

### 3. Run the Streamlit Application Host

Launch the application server to interact with your code modules locally at `localhost:8501`:

```bash
streamlit run CAPM_Return.py

```

```

```
