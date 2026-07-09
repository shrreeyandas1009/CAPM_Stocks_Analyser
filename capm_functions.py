import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Function to plot interactive plot
def interactive_plot(df):
    fig = go.Figure()
    for i in df.columns[1:]:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[i].values, name=str(i), mode='lines'))
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Function to normalize the prices based on the initial price
def normalize(df):
    x = df.copy()
    for i in x.columns[1:]:
        x[i] = x[i] / x[i].iloc[0] # Using .iloc ensures safe positional indexing
    return x

# Vectorized function to calculate the daily returns natively (Lightning Fast)
def daily_return(df):
    df_daily_return = df.copy()
    # Set Date as index temporarily so pct_change doesn't process it
    if 'Date' in df_daily_return.columns:
        df_daily_return.set_index('Date', inplace=True)
        
    # Standard math: calculate fractional daily percentage shifts directly
    df_daily_return = df_daily_return.pct_change()
    
    # Reset index and fill the very first row (NaN) with 0
    df_daily_return.reset_index(inplace=True)
    df_daily_return.fillna(0, inplace=True)
    return df_daily_return

# Function to calculate beta based on standard fractional returns
def calculate_beta(stocks_daily_return, stock):
    # Fit a 1st-degree polynomial (y = mx + c) where m is Beta, c is Alpha
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a
