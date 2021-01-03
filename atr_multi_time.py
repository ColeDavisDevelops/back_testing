from account import Account 
import datetime as dt

class AtrCrossPt(Account):

  def __init__(self, data, balance, period):

    super().__init__(balance)
    self.data = data

    
    self.format_data = {
      'open': [],
      'high': [],
      'low': [],
      'close': [],
      'date': [],
      'stop_loss': [], 
      'balance': [],
      'account_value': []
    }
    self.period = period
  
  @staticmethod
  def true_range(c,h,l,o,yc):
    x = h-l
    y = abs(h-yc)
    z = abs(l-yc)

    return max(x, y, z)

  @staticmethod
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

    for i in s[n+1:]:
      tmp = ( (i - ema[j]) * multiplier) + ema[j]
      j = j + 1
      ema.append(tmp)
    return ema

  def execute_strategy(self):
    true_ranges = []
    curr_trend = False
    stop_loss = 0
    stop_size = 0
    counter = 0
    for candle in self.data['candles']:
      self.format_data['open'].append(candle["open"])
      self.format_data['high'].append(candle["high"])
      self.format_data['low'].append(candle["low"])
      self.format_data['close'].append(candle["close"])
      self.format_data['date'].append(dt.datetime.fromtimestamp(candle["datetime"]/1000.0).strftime('%c'))

      self.format_data['account_value'].append(self.account_value(candle['close']))

      # if not day one
      if counter != 0: 
        # add atr
        tr = self.true_range(candle["open"], candle["high"], candle["low"], candle["open"], self.data['candles'][counter-1]["close"])
        true_ranges.append(tr)

        if len(true_ranges) > 10: 
          order_object = {'price': candle['close'], 'date': self.format_data['date'][-1]}

          if (candle["close"] < self.format_data["stop_loss"][-1]) and curr_trend == True:
            # trend changes down stop gets reset
            curr_trend = False
            self.format_data["stop_loss"].append(candle["close"] + self.exponential_average(true_ranges, self.period)[-1])
            stop_size = self.exponential_average(true_ranges, self.period)[-1]

            if self.position['shares'] > 0:
              self.sell(order_object)


            order_object["txn_type"] = "SELL"
            self.sell(order_object)

            self.format_data['balance'].append(self.balance)
            continue

          if (candle["close"] > self.format_data["stop_loss"][-1]) and curr_trend != True:
            curr_trend = True
            self.format_data["stop_loss"].append(candle["close"] - self.exponential_average(true_ranges, self.period)[-1])
            stop_size = self.exponential_average(true_ranges, self.period)[-1]


            if self.position['shares'] < 0:
              self.buy(order_object)

            order_object["txn_type"] = "BUY"
            self.buy(order_object)
            self.format_data['balance'].append(self.balance)
            continue
    
          if curr_trend: 

            if self.position['shares'] > 0:
              if self.orders[-1]['price'] + stop_size <= candle['close']:
                order_object["txn_type"] = "SELL"
                self.sell(order_object)

            # trailing stop = close - stop_size
            if (candle["close"] - stop_size) > self.format_data["stop_loss"][-1]:
              self.format_data["stop_loss"].append(candle["close"] - stop_size)
            else:
              self.format_data["stop_loss"].append(self.format_data["stop_loss"][-1])

          else:

            if self.position['shares'] < 0:
              if self.orders[-1]['price'] - stop_size >= candle['close']:
                order_object["txn_type"] = "BUY"
                self.buy(order_object)


            if (candle["close"] + stop_size) < self.format_data["stop_loss"][-1]:
              self.format_data["stop_loss"].append(candle["close"] + stop_size)
            else:
              self.format_data["stop_loss"].append(self.format_data["stop_loss"][-1])
            # closing price + 3 x atr

        else: 
          self.format_data['stop_loss'].append(0)

      else: 
        self.format_data['stop_loss'].append(0)
  
      self.format_data['balance'].append(self.balance)
      counter += 1

