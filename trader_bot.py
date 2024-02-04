from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader

from datetime import datetime

import fin_constants

BASE_URL = fin_constants.BASE_URL

ALPACA_CREDS = {
    "API_KEY": fin_constants.API_KEY,
    "API_SECRET": fin_constants.API_SECRET,
    "PAPER": True,
}

class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        
        return cash, last_price, quantity
        
        
    
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        
        if cash > last_price:
            if self.last_trade == None:
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.2,
                    stop_loss_limit_price=last_price*0.95
                )
                
                self.submit_order(order)
                self.last_trade = "buy"

start_date = datetime(2023,12,1)
end_date = datetime(2023,12,31)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name="StratOne", broker=broker, parameters={"symbol": "SPY", 
                                                                "cash_at_risk": 0.5})

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={}
)
#16:21