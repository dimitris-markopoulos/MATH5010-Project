# pip install yfinance
# pip install backtrader
# pip install pandas


import backtrader as bt
import yfinance as yf
import pandas as pd
import backtrader.feeds as btfeeds


df = yf.download('MSFT', start='2023-01-01', end='2023-12-31')
df.columns = df.columns.droplevel('Ticker')
data = btfeeds.PandasData(dataname=df)
df


class EMACrossoverStrategy(bt.Strategy):
    params = (
        ('short_ema', 10),
        ('long_ema', 30),
    )

    def __init__(self):
        self.ema_short = bt.ind.EMA(period=self.p.short_ema)
        self.ema_long = bt.ind.EMA(period=self.p.long_ema)
        self.crossover = bt.ind.CrossOver(self.ema_short, self.ema_long)
        self.order = None
        self.trade_log = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.long_trades = 0
        self.short_trades = 0
        self.total_profit = 0
        self.total_loss = 0
        self.max_drawdown = 0
        self.equity_curve = []
        self.highest_equity = self.broker.getvalue()
        self.last_trade_was_long = None


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return  # Do nothing yet

        if order.status in [order.Completed]:
            action = 'BUY' if order.isbuy() else 'SELL'
            self.log(f'{action} EXECUTED, Price: {order.executed.price:.2f}, Size: {order.executed.size}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            pnl = trade.pnl
            self.total_trades += 1
            self.total_profit += pnl if pnl > 0 else 0
            self.total_loss += pnl if pnl < 0 else 0
    
            if pnl > 0:
                self.winning_trades += 1
            else:
                self.losing_trades += 1
    
            if self.last_trade_was_long is True:
                self.long_trades += 1
            elif self.last_trade_was_long is False:
                self.short_trades += 1
            else:
                self.short_trades += 1
    
            self.trade_log.append({
                'date': self.datas[0].datetime.date(0),
                'gross': trade.pnl,
                'net': trade.pnlcomm,
                'price': trade.price
            })


    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} - {txt}')

    def print_report(self):
        print("\n====== STRATEGY REPORT ======")
        print(f"Total Trades       : {self.total_trades}")
        print(f"Winning Trades     : {self.winning_trades}")
        print(f"Losing Trades      : {self.losing_trades}")
        print(f"Win Rate           : {self.winning_trades / self.total_trades * 100:.2f}%" if self.total_trades else "N/A")
        print(f"Long Trades        : {self.long_trades}")
        print(f"Short Trades       : {self.short_trades}")
        print(f"Total Profit       : {self.total_profit:.2f}")
        print(f"Total Loss         : {self.total_loss:.2f}")
        print(f"Avg Win            : {self.total_profit / self.winning_trades:.2f}" if self.winning_trades else "N/A")
        print(f"Avg Loss           : {self.total_loss / self.losing_trades:.2f}" if self.losing_trades else "N/A")
        print(f"Max Drawdown       : {self.max_drawdown:.2f}")
        print(f"Final Portfolio Val: {self.broker.getvalue():.2f}")
        print("==============================")

    def next(self):
        if self.order:
            return  # Wait for previous order to complete

        if not self.position:
            if self.crossover > 0:
                self.log('BUY SIGNAL')
                self.order = self.buy()
                self.last_trade_was_long = True
        elif self.crossover < 0:
            self.log('SELL SIGNAL')
            self.order = self.sell()
            self.last_trade_was_long = False

            
        current_value = self.broker.getvalue()
        self.equity_curve.append(current_value)
        
        if current_value > self.highest_equity:
            self.highest_equity = current_value
        
        drawdown = self.highest_equity - current_value
        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown


cerebro = bt.Cerebro()
cerebro.addstrategy(EMACrossoverStrategy)
cerebro.adddata(data)
cerebro.broker.setcash(1000)

results = cerebro.run()
strategy = results[0]

# Get broker info
final_value = cerebro.broker.getvalue()
initial_cash = cerebro.broker.startingcash
profit = final_value - initial_cash

print(f"\nInitial Cash: {initial_cash}")
print(f"Final Portfolio Value: {final_value}")
print(f"Total Profit: {profit}")

print("\nTrade Log:")
for trade in strategy.trade_log:
   print(trade)