class Account:
  # commision 
  # max drawdown
  # std dev
  # variance
  # account peak
  # balance history []
    
  def __init__(self, balance):
    self.balance = balance
    self.orders = []
    self.balance_history = []

  def buy(self, order_object):
    self.orders.append(order_object)
    self.balance -= order_object['price']
    self.balance_history.append(self.balance)
    print('bought @ $%s, bal: %s' % (order_object['price'], self.balance))

  def sell(self, order_object):
    self.orders.append(order_object)
    self.balance += order_object['price']
    self.balance_history.append(self.balance)
    print('sold @ $%s, bal: %s' % (order_object['price'], self.balance))

