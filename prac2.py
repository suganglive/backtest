import pyupbit
import numpy as np
import pandas as pd

ss = {'btc': pyupbit.get_ohlcv("KRW-BTC", count=1582), 'eth': pyupbit.get_ohlcv("KRW-ETH", count=1582),
      'xrp': pyupbit.get_ohlcv("KRW-XRP", count=1582), 'ltc': pyupbit.get_ohlcv("KRW-ltc", count=1582)}

for i in ss:
    del ss[i]['volume'], ss[i]['value']
    ss[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close"]

dfs = pd.concat([ss['btc'], ss['eth'], ss['xrp'], ss['ltc']], axis=1)

dfs = dfs[['btc_open', 'eth_open', 'xrp_open', 'ltc_open', 'btc_high', 'eth_high', 'xrp_high', 'ltc_high',
           'btc_low', 'eth_low', 'xrp_low', 'ltc_low', 'btc_close', 'eth_close', 'xrp_close', 'ltc_close']]

k = 0.5
coins = ['btc', 'eth', 'xrp', 'ltc']
target_v = 0.05
slpy = 0.002

for i in coins:
    dfs[f'{i}_range'] = dfs[f'{i}_high'] - dfs[f'{i}_low'] 
    dfs[f'{i}_range'] = dfs[f'{i}_range'].shift(1)

for i in coins:
    dfs[f'{i}_range_r'] = (dfs[f'{i}_range'].shift(-1))/(dfs[f'{i}_open'])
    dfs[f'{i}_range_r'] = dfs[f'{i}_range_r'].shift(1)

print(dfs)

