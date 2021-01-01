# importing the requests library 
import requests 
import json
import pandas as pd
import datetime as dt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from atr_cross import AtrCross

# fetch data 
endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
params = {
  'apikey' : 'VR3OMPUFUABHGNBACPC7XGK8ARVIGTQD',
}

full_url = endpoint.format(stock_ticker='SPY',periodType='year',period=2,frequencyType='daily',frequency=1)

page = requests.get(url=full_url,
                    params=params)
# content = json.loads(page.content)

data = page.json()

#*************************************************

strat = AtrCross(data, 1000, 9)

strat.execute_strategy()

df = pd.DataFrame(data=strat.format_data)

df = df[12:]

fig = make_subplots(
  rows=2,
  cols=1,
  row_heights=[0.5, 0.2] 
  # specs=[[{"type": "candlestick", "rowspan": 2},
  #       {"type": "scatter"}]]
)

fig.add_trace(
  go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
  )
)


# fig = go.Figure(data=[go.Candlestick(x=df['date'],
#                 open=df['open'],
#                 high=df['high'],
#                 low=df['low'],
#                 close=df['close'])])

fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=(df['stop_loss'])
    ))  

fig.append_trace(
    go.Scatter(
      x=df['date'],
      y=df['balance']
    ), row=2, col=1)  
# print(df)
# print(strat.balance_history)

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()


