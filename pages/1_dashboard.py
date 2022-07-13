import streamlit as st
from datetime import date

import yfinance as yf
import pandas as pd
from prophet import Prophet # 為FaceBook所開發，用於預估週期性的數值變化，輸入時間與數值兩個欄位就會預估未來數值的變化。 #fbprophet to prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from plotly.subplots import make_subplots  

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


st.title('股票儀表板 (Stock Dashboard)')

stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', '0050.TW', '00885.TW')
selected_stocks = st.multiselect('請選擇想要選取的股票 (Select datasets for prediction)', stocks, default=[stocks[0],stocks[1]])
stock_dfs = pd.DataFrame()


@st.cache(allow_output_mutation=True)
def load_data(ticker):
    data = yf.download(ticker, START, TODAY) 
	# Date, Open, High, Low, Close, Adj Close, Volume
    data.reset_index(inplace=True)
    return data

# Plot line chart
def plot_line_chart_compare(data):
	fig = go.Figure()
	for a, b in stock_dfs.groupby("Company Name"):
		fig.add_trace(go.Scatter(x=b['Date'], y=b['Close'], name= a + "收盤價 (stock_close)"))
	fig.layout.update(title_text='收盤價歷史走勢比較 (Time Series data with Rangeslider)', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

# Plot subplots chart
def plot_subplots_chart_individual(data):
	fig = make_subplots(rows=len(selected_stocks)//2+1, cols=2,)
	for index, (a, b) in enumerate(data.groupby("Company Name")): 		
		fig.add_trace(go.Scatter(x=b['Date'], y=b['Close'], name= a + "收盤價 (stock_close)"),row=index//2+1, col=index%2+1)
		fig.layout.update(title_text='個股收盤價歷史走勢')
	st.plotly_chart(fig)


data_load_state = st.text('Loading data...')
for i in selected_stocks:
	data = load_data(i)
	data['Company Name']= i
	stock_dfs = pd.concat([stock_dfs, data])
data_load_state.text('Loading data... done!')


plot_line_chart_compare(stock_dfs)

plot_subplots_chart_individual(stock_dfs)





