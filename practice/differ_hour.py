#how to get a different timeline
import pyupbit
import numpy as np
import pandas as pd
import datetime

# btc = pyupbit.get_ohlcv("KRW-BTC", "minute60", count=3000, base=12)

# ss = {'btc': pyupbit.get_ohlcv("KRW-BTC", "minute60", count=1000)}

# btc = pyupbit.get_daily_ohlcv_from_base("KRW-BTC", offset=12)
# print(btc)
# ss['btc'][]

def get_daily_ohlcv_from_base(ticker="KRW-BTC", base=0):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        # df = pyupbit.get_ohlcv(ticker, interval="minute60", count=37898)
        df = pyupbit.get_ohlcv(ticker, interval="minute60")
        df = df.resample('24H', offset=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return df
    except Exception as x:
        return None

a = get_daily_ohlcv_from_base(ticker="KRW-BTC", base='0h')
print('a', a)

# b = pyupbit.get_ohlcv("KRW-BTC", count=3)
# print('b', b)

c = pyupbit.get_daily_ohlcv_from_base(ticker="KRW-BTC", base = 0)
print('c', c)