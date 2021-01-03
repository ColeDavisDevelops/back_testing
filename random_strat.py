from account import Account
import datetime as dt
import random

class RandomST(Account):

  def __init__(self, data, balance, period=9):
    super().__init__(balance)
    self.data = data  
    self.format_data = {
      'open': [],
      'high': [],
      'low': [],
      'close': [],
      'date': [],
      'balance': [],
      'account_value': []
    }
    self.period = period


  def execute_strategy(self):
    for candle in self.data['candles']:
      self.format_data['open'].append(candle["open"])
      self.format_data['high'].append(candle["high"])
      self.format_data['low'].append(candle["low"])
      self.format_data['close'].append(candle["close"])
      self.format_data['date'].append(dt.datetime.fromtimestamp(candle["datetime"]/1000.0).strftime('%c'))
      self.format_data['account_value'].append(self.account_value(candle['close']))

      order_object = {'price': candle['close'], 'date': self.format_data['date'][-1]}

      if random.randint(0, 1) == 0: 
        self.buy(order_object)
      if random.randint(0, 1) == 1: 
        self.sell(order_object)





