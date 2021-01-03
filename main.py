# importing the requests library 
import requests 
import json
import pandas as pd
import datetime as dt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from atr_cross import AtrCross
from atr_cross_pt import AtrCrossPt 
from random_strat import RandomST

# fetch data 
endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
params = {
  'apikey' : 'VR3OMPUFUABHGNBACPC7XGK8ARVIGTQD',
}

full_url = endpoint.format(stock_ticker='SPY',periodType='year',period=2,frequencyType='daily',frequency=1)
full_url_1 = endpoint.format(stock_ticker='SPY',periodType='month',period=6,frequencyType='daily',frequency=1)

page = requests.get(url=full_url,
                    params=params)
page2 = requests.get(url=full_url_1,
                    params=params)
# content = json.loads(page.content)

data = page.json()

data2 = page2.json()

#*************************************************

strat = AtrCross(data, 1000, 9)
strat2P1 = AtrCrossPt(data, 1000, 9)
strat2P2 = AtrCrossPt(data2, 1000, 9)
# strat3 = RandomST(data, 1000)


strat2P1.execute_strategy()
print("*******************************")
print("*******************************")
print("*******************************")
strat2P2.execute_strategy()
# print("*******************************")
# print("*******************************")
# print("*******************************")
# strat3.execute_strategy()

print(strat2P1.format_data["stop_loss"][-1])
print(strat2P2.format_data["stop_loss"][-1])


df = pd.DataFrame(data=strat2P1.format_data)

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

fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=(df['stop_loss'])
    ))  

fig.append_trace(
    go.Scatter(
      x=df['date'],
      y=df['account_value']
    ), row=2, col=1)  
# print(df)
# print(strat.balance_history)

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()


