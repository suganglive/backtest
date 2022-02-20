import pyupbit
import numpy as np
import pandas as pd

ss = {'btc': pyupbit.get_ohlcv("KRW-BTC", count=8), 'eth': pyupbit.get_ohlcv("KRW-ETH", count=8),
      'xrp': pyupbit.get_ohlcv("KRW-XRP", count=8), 'ltc': pyupbit.get_ohlcv("KRW-eth", count=8)}

for i in ss:
    del ss[i]['volume'], ss[i]['value']
    ss[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close"]

dfs = pd.concat([ss['btc'], ss['eth'], ss['xrp'], ss['ltc']], axis=1)
dfs['k'] = 0.5
coins = ['btc', 'eth', 'xrp', 'ltc']

for i in coins:
    dfs[f'{i}_y_range'] = (dfs[f'{i}_high'] - dfs[f'{i}_low']).shift(1)

for i in coins:
    dfs[f'{i}_target'] = dfs[f'{i}_open'] + (dfs[f'{i}_y_range'] * dfs['k'])

for i in coins:
    dfs[f'{i}_target_s'] = np.where(
        dfs[f'{i}_high'] > dfs[f'{i}_target'], 1, 0)

for i in coins:
    dfs[f'{i}_ma5_s'] = np.where(
        dfs[f'{i}_open'] >= dfs[f'{i}_open'].rolling(window=5).mean(), 1, 0)

for i in coins:
    dfs[f'{i}_R'] = dfs[f'{i}_close']/dfs[f'{i}_target'] - 1

dfs['P_R'] = dfs['btc_R'] * dfs['btc_target_s'] * dfs['btc_ma5_s'] + dfs['eth_R'] * dfs['eth_target_s'] * dfs['eth_ma5_s'] + \
    dfs['xrp_R'] * dfs['xrp_target_s'] * dfs['xrp_ma5_s'] + \
    dfs['ltc_R'] * dfs['ltc_target_s'] * dfs['ltc_ma5_s']



# dfs.to_excel("kimchi.xlsx")

print(dfs)
