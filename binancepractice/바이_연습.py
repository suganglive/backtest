import ccxt
import numpy as np
import pandas as pd
from datetime import *

binance = ccxt.binance()

def get_daily_ohlcv_from_base(ticker, base = "10h"):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        df = binance.fetch_ohlcv(symbol = ticker, timeframe='1h', limit=120)
        for i in df:
            i[0] = datetime.fromtimestamp(i[0]/1000).strftime('%Y-%m-%d %H:%M:%S')
            del i[-1]
        df = pd.DataFrame(df, columns =['date', 'open', 'high', 'low', 'close'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.resample('24H', offset=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        return df
    except Exception as x:
        print(x)
        return None

df = get_daily_ohlcv_from_base("BTC/USDT")
print(df)
# binance = ccxt.binance()
# df = binance.fetch_ohlcv("BTC/USDT", "1h", limit=120)
# for i in df:
#     i[0] = datetime.fromtimestamp(i[0]/1000).strftime('%Y-%m-%d %H:%M:%S')
#     del i[-1]
# df = pd.DataFrame(df, columns =['date', 'open', 'high', 'low', 'close']).set_index('date')
# # print(df)

