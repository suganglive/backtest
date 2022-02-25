import ccxt
from matplotlib import ticker
import pandas as pd
import numpy as np
import datetime
import pyupbit

tickers = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT']
start_date = int(datetime.datetime(2018, 1, 1, 10, 20).timestamp() * 1000)

# for i in tickers:
#     binance = ccxt.binance()
#     btc_ohlcv = binance.fetch_ohlcv(i, timeframe='1d')
#     df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
#     df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#     print(df)

def get_daily_ohlcv_from_base(base=0):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        df = pd.read_excel("/Users/sugang/Documents/GitHub/backtest/backtestdata/bi_btc_h.xlsx", index_col=0)
        # df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=37898)
        df = df.resample('24H', offset=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        return df
    except Exception as x:
        return None

dfs = get_daily_ohlcv_from_base(base='11h')
dfs.to_excel("bi_11h.xlsx")
#/Users/sugang/Documents/GitHub/backtest/backtestdata

# df1 = pd.read_excel("/Users/sugang/Documents/GitHub/backtest/backtestdata/bi_btc_hh.xlsx", index_col=0)
# # df3 = pd.DataFrame({'open':df1['open'], 'high':df1['high'], 'low':df1['low'], 'close':df1['close']})
# # df1.reset_index(drop=False)
# print(df1)
# # print(df3)
# df2 = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=123)
# print(df2)
