from cmath import e
import pyupbit
import pandas as pd
import numpy as np
# import logging

# logging.basicConfig(filename='upbit8.log', level=logging.INFO, format='%(created)f:%(message)s')

# tickers = pyupbit.get_tickers("KRW")
tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP']

dct = {}
df = pd.DataFrame()
for ticker in tickers:
    try:
        dct[ticker] = pyupbit.get_ohlcv(ticker, interval='day', count=365)
        del dct[ticker]['value']
        dct[ticker].columns = [f"{ticker}_open", f"{ticker}_high", f"{ticker}_low", f"{ticker}_close", f"{ticker}_volume"]
        vol1 = dct[ticker][f"{ticker}_volume"].rolling(window=5).mean()
        close = dct[ticker][f"{ticker}_close"].rolling(window=5).mean()
        vol2 = vol1 * close
        dct[ticker][f"{ticker}_volume"] = vol2
        df = pd.concat([df, dct[ticker]], axis=1)
    except Exception as e:
        print(ticker, ' error :', str(e))
# df.to_excel("220309.xlsx")

df2 = df
for ticker in tickers:
    del df2[f'{ticker}_open'], df2[f'{ticker}_high'], df2[f'{ticker}_low'], df2[f'{ticker}_close']

df2.columns = tickers
df2 = df2.rank(method='min', ascending=False, axis=1)


df = pd.concat([df, df2], axis=1)
print(df)