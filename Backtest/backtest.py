from strategy import *
from indicators import *

class BacktestEngine:
    def __init__(self):
        self.data = None
        self.strategy = None
        self.results = None

    def set_data(self, data):
        """Set the market data for backtesting."""
        self.data = data


    def set_strategy(self, strategy):
        self.strategy = strategy


    def run(self):
        if self.data is None and self.strategy is None:
            raise ValueError("Data and Strategy can not be None")
        strategy = self.strategy(self.data)
        for index in range(len(self.data)):
            strategy.next(index)

        return strategy.close()
        
    def report(self):
        if self.results is None:
            raise ValueError("No results to report")
        


import pandas as pd
def run_backtest():
    data = pd.read_csv('data.csv') 
    timeframe = '5min'
    data = Indicators.resample(data, timeframe)
    data = Indicators.ema(data, 10, 'ema'+timeframe)
    data = Indicators.supertrend(data, 10, 3, 'supertrend'+timeframe)
    data = Indicators.vwap(data, 'vwap'+timeframe)
    data = Indicators.local_maxima(data, 11)
    data = Indicators.local_minima(data, 11)
    print(data[['timestamp', 'maxima', 'minima']].tail(50))
    # engine = BacktestEngine()
    # engine.set_data(data)
    # engine.set_strategy(MACrossoverStrategy)
    # results = engine.run()
    # for i in results:
    #     print(i)
    # print(results)
    # print(type(results))

run_backtest()