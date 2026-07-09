# importing libraries
import streamlit as st
import datetime
import pandas_datareader.data as web
import yfinance as yf
import pandas as pd
import capm_functions
import numpy as np
import plotly.express as px

# setting page config
st.set_page_config(
    page_title="CAPM - Calculate Beta",
    page_icon="📈",
    layout="wide",
)

st.title('Calculate Beta and Return for Individual Stock')

# getting input from user
col1, col2 = st.columns([1, 1])
with col1:
    stock = st.selectbox("Choose a stock", ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'))
with col2:
    year = st.number_input("Number of Years", 1, 10, value=2)

# downloading data for SP500 & Stock
end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day)

# Download benchmark (FRED)
SP500 = web.DataReader(['sp500'], 'fred', start, end)
SP500.reset_index(inplace=True)
SP500.columns = ['Date', 'sp500']
SP500['Date'] = pd.to_datetime(SP500['Date'])

# Download chosen stock cleanly
data = yf.download(stock, start=start, end=end, group_by='ticker')

stocks_df = pd.DataFrame()
if isinstance(data.columns, pd.MultiIndex):
    stocks_df[stock] = data[(stock, 'Close')]
else:
    stocks_df[stock] = data['Close']

stocks_df.reset_index(inplace=True)

# Format and strip timezones to allow an exact matching inner merge
stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.tz_localize(None)
stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

# Set Date as index before math transformations
stocks_df.set_index('Date', inplace=True)

# ==============================================================================
# CALIBRATED FINANCIAL MATH (THE PERCENTAGE FIX)
# ==============================================================================
# Calculate percentage returns instead of raw price transformations
stocks_daily_return = stocks_df.pct_change().dropna()

# Annualized Market Return (Mean Daily Return * 252 Trading Days * 100 for %)
rm = stocks_daily_return['sp500'].mean() * 252 * 100

# Calculate beta and alpha using percentage data frames
beta, alpha = capm_functions.calculate_beta(stocks_daily_return, stock)

# Market risk-free benchmark rate (Current US 10-Year Treasury Yield ~ 4.2%)
rf = 4.2

# Calculate final expected asset return using standard CAPM
return_value = round(rf + (beta * (rm - rf)), 2)

# ==============================================================================
# UI VISUALIZATION LAYOUT
# ==============================================================================# 
# --- Find these lines in pages/Calculate_Beta.py and update them ---

st.markdown(f'### **Asset Beta ($\beta$):** `{round(beta, 2)}`')
st.markdown(f'### **Annualized Market Return ($R_m$):** `{round(rm, 2)}%`')
st.markdown(f'### **CAPM Projected Annual Return ($E(R_i)$):** `{return_value}%`')

# Re-plot the scatter graph using calibrated percentage values
fig = px.scatter(
    stocks_daily_return, 
    x='sp500', 
    y=stock, 
    title=f"{stock} Daily Variance Profile vs. S&P 500 Market Matrix",
    labels={'sp500': 'S&P 500 Daily Return', stock: f'{stock} Daily Return'}
)

# Overlay the OLS Regression Trendline safely
fig.add_scatter(
    x=stocks_daily_return['sp500'], 
    y=beta * stocks_daily_return['sp500'] + alpha,  
    mode='lines',
    line=dict(color="crimson", width=2),
    name='OLS CAPM Regression Line'
)

st.plotly_chart(fig, use_container_width=True)
