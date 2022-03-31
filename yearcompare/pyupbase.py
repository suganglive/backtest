import pyupbit
import numpy as np
import pandas as pd

# tickers = pyupbit.get_tickers("KRW")
# hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
# dct = {}

def get_daily_ohlcv_from_base(ticker="KRW-BTC", base='10h'):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        # df = pyupbit.get_ohlcv(ticker, interval="minute60", count=17520) # 2 years
        df = pyupbit.get_ohlcv(ticker, interval="minute60", count=8760) # 1 years
        # df = pyupbit.get_ohlcv(ticker, interval="minute60", count=300)
        df = df.resample('24H', offset=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return df
    except Exception as e:
        print(e)
        return None


# for h in hours:
#     for i in tickers:
#         dct[i] = get_daily_ohlcv_from_base(ticker=i, base=h)
#         dct[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close", f"{i}_vol"]
#     a.to_excel(f'/Users/sugang/Documents/GitHub/backtest/220326/data_{h}.xlsx')
