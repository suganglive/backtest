import pyupbit
import pandas as pd

df = pyupbit.get_ohlcv("KRW-BTC")
df.drop('value', axis=1)
del df['value']
print(df)