import pyupbit
import numpy as np
import pandas as pd

# btc: pyupbit.get_ohlcv("KRW-BTC", count=1580)
# eth: pyupbit.get_ohlcv("KRW-ETH", count=1580)
# xrp: pyupbit.get_ohlcv("KRW-XRP", count=1580)
# ltc: pyupbit.get_ohlcv("KRW-eth", count=1580)

ss = {'btc' : pyupbit.get_ohlcv("KRW-BTC", count=8), 'eth' : pyupbit.get_ohlcv("KRW-ETH", count=8),
      'xrp' : pyupbit.get_ohlcv("KRW-XRP", count=8), 'ltc' : pyupbit.get_ohlcv("KRW-eth", count=8)}

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
    dfs[f'{i}_target_s'] = np.where(dfs[f'{i}_high'] > dfs[f'{i}_target'], 1, 0)

for i in coins:
    dfs[f'{i}_ma5_s'] = np.where(dfs[f'{i}_open'] >= dfs[f'{i}_open'].rolling(window=5).mean(), 1, 0)


dfs.to_excel("kimchi.xlsx")

print(dfs)


# for i in ss:
#     del i['volume'], i['value']

# btc.columns = ["btc_open", "btc_high", "btc_low", "btc_close"]
# eth.columns = ["eth_open", "eth_high", "eth_low", "eth_close"]
# xrp.columns = ["xrp_open", "xrp_high", "xrp_low", "xrp_close"]
# ltc.columns = ["ltc_open", "ltc_high", "ltc_low", "ltc_close"]

# dfs = pd.concat([btc, eth, xrp, ltc], axis=1)

# print(dfs)
# # dfs.to_excel("lol.xlsx")
