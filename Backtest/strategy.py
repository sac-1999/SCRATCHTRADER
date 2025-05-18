
import numpy as np
class BaseStrategy:
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.trades = []

    def init(self):
        pass

    def next(self, index):
        pass

    def close(self):
        return self.trades
    
class MACrossoverStrategy(BaseStrategy):
    def __init__(self, data, short_window=10, long_window=30):
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
        self.data['short_ma'] = self.data['close'].rolling(window=short_window).mean()
        self.data['long_ma'] = self.data['close'].rolling(window=long_window).mean()

    def next(self, index):
        if index < self.long_window:
            return

        if self.position == 0:
            if self.data['short_ma'][index] > self.data['long_ma'][index]:
                self.position = 1
                self.trades.append(('BUY', self.data.loc[index]))

        elif self.position == 1:
            if self.data['short_ma'][index] < self.data['long_ma'][index]:
                self.position = 0
                self.trades.append(('SELL', self.data.loc[index]))


class WpatternStrategy(BaseStrategy):
    def __init__(self, df, day = True):
        super().__init__(df)
        df['day'] = df['timestamp'].apply(lambda x: x[:10]) 
        df['minima'] = np.where(df['minima'], df['low'], np.nan)
        df['maxima'] = np.where(df['maima'], df['high'], np.nan)
        df['minima'] = df['minima'].ffill()
        df['maxima'] = df['maxima'].ffill()
        df['dayhigh'] = df.groupby('day')['high'].transform('max')
        df['daylow'] = df.groupby('day')['low'].transform('min')
        prev_day_high_low = self.df.groupby('day').agg(
            dayhigh=('high', 'max'),
            daylow=('low', 'min')
        ).shift(1)

        df = df.merge(prev_day_high_low, left_on='day', right_index=True, how='left', suffixes=('', '_prev'))


    def next(self, index):
        if index < self.long_window:
            return

        if self.position == 0:
            if self.data['short_ma'][index] > self.data['long_ma'][index]:
                self.position = 1
                self.trades.append(('BUY', self.data.loc[index]))

        elif self.position == 1:
            if self.data['short_ma'][index] < self.data['long_ma'][index]:
                self.position = 0
                self.trades.append(('SELL', self.data.loc[index]))


    def transform(data):
        df['day'] = df['timestamp'].apply(lambda x: x[:10]) 
        df['minima'] = np.where(df['minima'], df['low'], np.nan)
        df['maxima'] = np.where(df['maima'], df['high'], np.nan)
        df['minima'] = df['minima'].ffill()
        df['maxima'] = df['maxima'].ffill()
        df['dayhigh'] = df.groupby('day')['high'].transform('max')
        df['daylow'] = df.groupby('day')['low'].transform('min')
        prev_day_high_low = df.groupby('day').agg(
            dayhigh=('high', 'max'),
            daylow=('low', 'min')
        ).shift(1)

        df = df.merge(prev_day_high_low, left_on='day', right_index=True, how='left', suffixes=('', '_prev'))




