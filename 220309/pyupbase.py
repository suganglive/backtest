import pyupbit
import numpy as np
import pandas as pd

def get_daily_ohlcv_from_base(ticker="KRW-BTC", base='10h'):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        df = pyupbit.get_ohlcv(ticker, interval="minute60", count=8760)
        df = df.resample('24H', offset=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return df
    except Exception as e:
        print(e)
        return None