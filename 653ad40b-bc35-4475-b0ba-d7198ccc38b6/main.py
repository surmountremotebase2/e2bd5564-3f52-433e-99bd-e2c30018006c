from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Here you might want to initialize any necessary variables or settings
        self.ticker = "BTC"

    @property
    def assets(self):
        # List of assets this strategy trades
        return [self.ticker]

    @property
    def interval(self):
        # Setting the data interval to daily
        return "1day"

    def run(self, data):
        # Calculate the RSI for Bitcoin using a commonly used period of 14 days
        btc_rsi = RSI(self.ticker, data["ohlcv"], length=14)

        if not btc_rsi:
            return TargetAllocation({self.ticker: 0})

        # The current RSI reading is the last value in the RSI list
        current_rsi = btc_rsi[-1]
        log(f"Current RSI for {self.ticker}: {current_rsi}")

        allocation = 0

        # Criteria for buying
        if current_rsi < 30:
            log("RSI below 30, buying signal")
            allocation = 1  # 100% allocation to BTC
        
        # Criteria for selling or going neutral
        elif current_rsi > 70:
            log("RSI above 70, selling signal")
            allocation = 0  # 0% allocation, effectively moving to cash or equivalent
        
        # Return the target allocation for the strategy
        return TargetAllocation({self.ticker: allocation})