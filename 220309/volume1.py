import pyupbit
import operator
import pandas as pd
import numpy as np

# tickers = pyupbit.get_tick_size()
tickers = pyupbit.get_tickers("KRW")

coins = ['coin1', 'coin2', 'coin3', 'coin4', 'coin5']
dct = {}
df = pd.DataFrame()
# for i in range(1,366):
for tick in tickers:
    data = pyupbit.get_ohlcv(tick, count=365)
    try:
        vol1 = data['volume'].rolling(window=5).mean()
        close = data['close'].rolling(window=5).mean()
        vol2 = vol1 * close
        dct[tick] = vol2[-1]
    except:
        print(f"{tick}_error")


# for c in coins:
    # df[c] = 
# sorted_d = dict(sorted(dct.items(), key=operator.itemgetter(1), reverse=True))
# a = list(sorted_d.keys())[:5]
# print(a)
