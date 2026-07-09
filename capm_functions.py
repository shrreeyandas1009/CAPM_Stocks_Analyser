import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Function to plot interactive plot
def interactive_plot(df):
    fig = go.Figure()
    for i in df.columns[1:]:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[i].values, name=str(i), mode='lines'))
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Function to normalize the prices based on the initial price
def normalize(df):
    x = df.copy()
    for i in x.columns[1:]:
        x[i] = x[i] / x[i].iloc[0]
    return x

# Vectorized function to calculate fractional daily returns
def daily_return(df):
    df_daily_return = df.copy()
    if 'Date' in df_daily_return.columns:
        df_daily_return.set_index('Date', inplace=True)
    df_daily_return = df_daily_return.pct_change()
    df_daily_return.reset_index(inplace=True)
    df_daily_return.fillna(0, inplace=True)
    return df_daily_return

# Function to calculate beta using OLS linear regression
def calculate_beta(stocks_daily_return, stock):
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a
