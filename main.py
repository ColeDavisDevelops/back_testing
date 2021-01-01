# importing the requests library 
import requests 
import json
import pandas as pd
import datetime as dt
import numpy as np
import plotly.graph_objects as go

# fetch data 
endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
params = {
  'apikey' : 'VR3OMPUFUABHGNBACPC7XGK8ARVIGTQD',
}

full_url = endpoint.format(stock_ticker='AAPL',periodType='day',period=1,frequencyType='minute',frequency=1)

page = requests.get(url=full_url,
                    params=params)
# content = json.loads(page.content)

data = page.json()

#*************************************************


# graph the data and maybe ATR 

format_data = {
  'open': [],
  'high': [],
  'low': [],
  'close': [],
  'date': [],
  'atrts': [],
  'stop_loss': []
}

true_ranges = []
period = 9
curr_trend = False 

def true_range(c,h,l,o,yc):
  x = h-l
  y = abs(h-yc)
  z = abs(l-yc)

  return max(x, y, z)


def exponential_average(s, n):
    """
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    """
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema

print(data)
stop_loss = 0
stop_size = 0
counter = 0
for candle in data['candles']:
  format_data['open'].append(candle["open"])
  format_data['high'].append(candle["high"])
  format_data['low'].append(candle["low"])
  format_data['close'].append(candle["close"])
  format_data['date'].append(dt.datetime.fromtimestamp(candle["datetime"]/1000.0).strftime('%c'))


  # if not day one
  if counter != 0: 
    # add atr
    tr = true_range(candle["open"], candle["high"], candle["low"], candle["open"], data['candles'][counter-1]["close"])
    true_ranges.append(tr)

    if len(true_ranges) > 10: 
      format_data['atrts'].append(exponential_average(true_ranges, period)[-1])


      if (candle["close"] < format_data["stop_loss"][-1]) and curr_trend == True:
        # trend changes down stop gets reset
        curr_trend = False
        format_data["stop_loss"].append(candle["close"] + exponential_average(true_ranges, period)[-1])
        stop_size = exponential_average(true_ranges, period)[-1]
        continue

      if (candle["close"] > format_data["stop_loss"][-1]) and curr_trend != True:
        curr_trend = True
        format_data["stop_loss"].append(candle["close"] - exponential_average(true_ranges, period)[-1])
        stop_size = exponential_average(true_ranges, period)[-1]
        continue
    
    
      if curr_trend: 
        # trailing stop = close - stop_size
        if (candle["close"] - stop_size) > format_data["stop_loss"][-1]:
          format_data["stop_loss"].append(candle["close"] - stop_size)
        else:
          format_data["stop_loss"].append(format_data["stop_loss"][-1])

      
      else: 
        if (candle["close"] + stop_size) < format_data["stop_loss"][-1]:
          format_data["stop_loss"].append(candle["close"] + stop_size)
        else:
          format_data["stop_loss"].append(format_data["stop_loss"][-1])
        # closing price + 3 x atr




    else: 
      format_data['atrts'].append(candle['high'] - candle['low'])     
      format_data['stop_loss'].append(0)

  else: 
    format_data['atrts'].append(candle['high'] - candle['low'])
    format_data['stop_loss'].append(0)
  
  counter += 1

df = pd.DataFrame(data=format_data)

df = df[12:]

fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=(df['stop_loss'])
    ))

# print(df)

fig.show()


