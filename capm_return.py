import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
import capm_functions

st.set_page_config(
    page_title="CAPM Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title('Capital Asset Pricing Model 📈')

col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect("Choose Stocks", ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'), ['TSLA', 'AAPL', 'MSFT', 'NFLX'], key="stock_list")
with col2:
    year = st.number_input("Number of Years", 1, 10, value=2)

if stocks_list:
    try:
        end = datetime.date.today()
        start = datetime.date(end.year - year, end.month, end.day)

        # 1. Download benchmark (S&P 500) from yfinance directly
        sp500_raw = yf.download('^GSPC', start=start, end=end, group_by='ticker')
        SP500 = pd.DataFrame()
        if isinstance(sp500_raw.columns, pd.MultiIndex):
            SP500['sp500'] = sp500_raw[('^GSPC', 'Close')]
        else:
            SP500['sp500'] = sp500_raw['Close']
        SP500.reset_index(inplace=True)
        SP500['Date'] = pd.to_datetime(SP500['Date']).dt.tz_localize(None)

        # 2. Download selected equities data cleanly
        stocks_df = pd.DataFrame()
        for stock in stocks_list:
            data = yf.download(stock, start=start, end=end, group_by='ticker')
            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    stocks_df[stock] = data[(stock, 'Close')]
                else:
                    stocks_df[stock] = data['Close']

        stocks_df.reset_index(inplace=True)
        stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.tz_localize(None)
        
        # Merge datasets synchronously
        stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

        # Data Frames Presentation Rows
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Dataframe Head')
            st.dataframe(stocks_df.head(), use_container_width=True)
        with col2:
            st.markdown('### Dataframe Tail')
            st.dataframe(stocks_df.tail(), use_container_width=True)

        # Graphs Presentation Rows
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Price of all the Stocks')
            st.plotly_chart(capm_functions.interactive_plot(stocks_df), use_container_width=True)
        with col2:
            st.markdown('### Price of all the Stocks (After Normalizing)')
            st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)), use_container_width=True)

        # Calibrated Financial Calculations Matrix
        stocks_daily_return = capm_functions.daily_return(stocks_df)

        beta = {}
        alpha = {}
        for i in stocks_daily_return.columns:
            if i != 'Date' and i != 'sp500':
                b, a = capm_functions.calculate_beta(stocks_daily_return, i)
                beta[i] = b
                alpha[i] = a

        # Render Beta Table Data Frames
        beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
        beta_df['Stock'] = beta.keys()
        beta_df['Beta Value'] = [round(val, 2) for val in beta.values()]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Calculated Beta Value')
            st.dataframe(beta_df, use_container_width=True)

        # Evaluate expected asset yields using strict CAPM metrics
        rf = 4.2  
        rm = stocks_daily_return['sp500'].mean() * 252 * 100  
        
        return_df = pd.DataFrame()
        stock_names = []
        return_values = []
        
        for stock, b_val in beta.items():
            stock_names.append(stock)
            calc_return = rf + (b_val * (rm - rf))
            return_values.append(f"{round(calc_return, 2)}%")
            
        return_df['Stock'] = stock_names
        return_df['Return Value (CAPM)'] = return_values

        with col2:
            st.markdown('### Calculated Return using CAPM')
            st.dataframe(return_df, use_container_width=True)

    except Exception as e:
        st.error(f"Pipeline running exception encountered: {e}")
else:
    st.warning("Please choose stock targets inside your portfolio selector widget to compute calculations.")
