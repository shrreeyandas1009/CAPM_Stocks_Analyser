# importing libraries
import streamlit as st
import pandas_datareader.data as web
import datetime
import pandas as pd
import yfinance as yf
import capm_functions

# setting page config
st.set_page_config(
    page_title="CAPM Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title('Capital Asset Pricing Model 📈')

# getting input from user
col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect("Choose Stocks", ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'), ['TSLA', 'AAPL', 'MSFT', 'NFLX'], key="stock_list")
with col2:
    year = st.number_input("Number of Years", 1, 10, value=2)

if stocks_list:
    try:
        # 1. Download benchmark data for SP500 (FRED is timezone-naive)
        end = datetime.date.today()
        start = datetime.date(end.year - year, end.month, end.day)
        SP500 = web.DataReader(['sp500'], 'fred', start, end)
        SP500.reset_index(inplace=True)
        SP500.columns = ['Date', 'sp500']
        SP500['Date'] = pd.to_datetime(SP500['Date'])

        # 2. Download data for chosen stocks cleanly
        stocks_df = pd.DataFrame()
        for stock in stocks_list:
            data = yf.download(stock, start=start, end=end, group_by='ticker')
            
            if not data.empty:
                # Handle modern multi-index headers from yfinance safely
                if isinstance(data.columns, pd.MultiIndex):
                    stocks_df[stock] = data[(stock, 'Close')]
                else:
                    stocks_df[stock] = data['Close']

        stocks_df.reset_index(inplace=True)
        
        # Standardize formatting and strip timezones to unlock precise inner joins
        stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.tz_localize(None)
        stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

        # Raw Previews Layout
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Dataframe Head')
            st.dataframe(stocks_df.head(), use_container_width=True)
        with col2:
            st.markdown('### Dataframe Tail')
            st.dataframe(stocks_df.tail(), use_container_width=True)

        # Charts Processing Layout
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Price of all the Stocks')
            st.plotly_chart(capm_functions.interactive_plot(stocks_df), use_container_width=True)

        with col2:
            st.markdown('### Price of all the Stocks (After Normalizing)')
            st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)), use_container_width=True)

        # ==============================================================================
        # CALIBRATED FINANCIAL MATH WORKFLOW
        # ==============================================================================
        # Convert absolute pricing metrics to clean daily percentage variations
        stocks_daily_return = capm_functions.daily_return(stocks_df)

        beta = {}
        alpha = {}

        for i in stocks_daily_return.columns:
            # Drop structural non-equity control columns
            if i != 'Date' and i != 'sp500':
                b, a = capm_functions.calculate_beta(stocks_daily_return, i)
                beta[i] = b
                alpha[i] = a

        # Render Beta Table Visuals
        beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
        beta_df['Stock'] = beta.keys()
        beta_df['Beta Value'] = [str(round(val, 2)) for val in beta.values()]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Calculated Beta Value')
            st.dataframe(beta_df, use_container_width=True)

        # Calculate expected asset yields using strict CAPM boundaries
        rf = 4.2  # Real-world benchmark Risk-Free Rate (~4.2% US Treasury Yield)
        rm = stocks_daily_return['sp500'].mean() * 252 * 100  # Annualized market index yield in %
        
        return_df = pd.DataFrame()
        stock_list = []
        return_value = []
        
        for stock, b_val in beta.items():
            stock_list.append(stock)
            # Evaluate expected returns using financial percentage baselines
            calc_return = rf + (b_val * (rm - rf))
            return_value.append(f"{round(calc_return, 2)}%")
            
        return_df['Stock'] = stock_list
        return_df['Return Value (CAPM)'] = return_value

        with col2:
            st.markdown('### Calculated Return using CAPM')
            st.dataframe(return_df, use_container_width=True)

    except Exception as e:
        st.error(f"Pipeline error encountered during execution: {e}")
        st.info("Please verify the structural code inside capm_functions.py is using daily variance profiles.")
else:
    st.warning("Please select at least one stock to start computing analytics.")
