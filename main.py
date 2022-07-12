# https://www.youtube.com/watch?v=0E_31WqVzCY&list=PLUmoPMqc-AQO_p9nYmiI8qUvKKcVMU7FF&index=1

import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet # 為FaceBook所開發，用於預估週期性的數值變化，輸入時間與數值兩個欄位就會預估未來數值的變化。 #fbprophet to prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('股價預測APP (Stock Forecast App)')

stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', '0050.TW')
selected_stock = st.selectbox('請選擇一檔股票 (Select dataset for prediction)', stocks)

n_years = st.slider('想要預測多少年(Years of prediction):', 1, 4)
st.text('本頁為透過 FaceBook 開發之 prophet 套件做預測')
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY) 
	# Date, Open, High, Low, Close, Adj Close, Volume
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="開盤價 (stock_open)"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="收盤價 (stock_close)"))
	fig.layout.update(title_text='歷史走勢 (Time Series data with Rangeslider)', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
	
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('預測資料 (Forecast data)')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)