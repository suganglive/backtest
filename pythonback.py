import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC")
df['range'] = df['high'] - df['low']
df['k'] = 0.5
df['target'] = df['open'] + (df['range'].shift(1) * df['k'])
df.to_excel("btc.xlsx")