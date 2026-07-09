import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
import capm_functions
import plotly.express as px

st.set_page_config(
    page_title="CAPM - Calculate Beta",
    page_icon="📈",
    layout="wide",
)

st.title('Calculate Beta and Return for Individual Stock')

col1, col2 = st.columns([1, 1])
with col1:
    stock = st.selectbox("Choose a stock", ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'))
with col2:
    year = st.number_input("Number of Years", 1, 10, value=2)

try:
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)

    # 1. Download market benchmark (S&P 500) via yfinance
    sp500_raw = yf.download('^GSPC', start=start, end=end, group_by='ticker')
    SP500 = pd.DataFrame()
    if isinstance(sp500_raw.columns, pd.MultiIndex):
        SP500['sp500'] = sp500_raw[('^GSPC', 'Close')]
    else:
        SP500['sp500'] = sp500_raw['Close']
    SP500.reset_index(inplace=True)
    SP500['Date'] = pd.to_datetime(SP500['Date']).dt.tz_localize(None)

    # 2. Download stock closing data assets cleanly
    data = yf.download(stock, start=start, end=end, group_by='ticker')
    stocks_df = pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        stocks_df[stock] = data[(stock, 'Close')]
    else:
        stocks_df[stock] = data['Close']
    stocks_df.reset_index(inplace=True)
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.tz_localize(None)

    # Merge dataset variables
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # Convert absolute pricing maps to performance changes
    stocks_daily_return = capm_functions.daily_return(stocks_df)

    # Mathematical Equation Modeling
    rm = stocks_daily_return['sp500'].mean() * 252 * 100
    beta, alpha = capm_functions.calculate_beta(stocks_daily_return, stock)
    rf = 4.2
    return_value = round(rf + (beta * (rm - rf)), 2)

    # Render LaTeX Equations Strings cleanly without raw formatting bugs
    st.markdown(f'### **Asset Beta ($\beta$):** `{round(beta, 2)}`')
    st.markdown(f'### **Annualized Market Return ($R_m$):** `{round(rm, 2)}%`')
    st.markdown(f'### **CAPM Projected Annual Return ($E(R_i)$):** `{return_value}%`')

    # OLS distribution graph modeling
    fig = px.scatter(
        stocks_daily_return, 
        x='sp500', 
        y=stock, 
        title=f"{stock} Daily Variance Profile vs. S&P 500 Market Matrix",
        labels={'sp500': 'S&P 500 Daily Return', stock: f'{stock} Daily Return'}
    )

    fig.add_scatter(
        x=stocks_daily_return['sp500'], 
        y=beta * stocks_daily_return['sp500'] + alpha,  
        mode='lines',
        line=dict(color="crimson", width=2),
        name='OLS CAPM Regression Line'
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error executing math visualization: {e}")
