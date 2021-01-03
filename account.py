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
    self.position = {'shares': 0}

  def buy(self, order_object):
    self.orders.append(order_object)
    self.balance -= order_object['price']
    self.balance_history.append(self.balance)
    self.position['shares'] += 1
    print('bought @ $%s, account val: %s, shares %s' % (order_object['price'], self.account_value(order_object['price']), self.position['shares']))

  def sell(self, order_object):
    self.orders.append(order_object)
    self.balance += order_object['price']
    self.balance_history.append(self.balance)
    self.position['shares'] -= 1
    print('sold @ $%s, account val: %s, shares %s' % (order_object['price'], self.account_value(order_object['price']), self.position['shares']))
    
  def account_value(self, curr_price):
    # print(self.position["shares"])
    return self.balance + curr_price * self.position["shares"]


