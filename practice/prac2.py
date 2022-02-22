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

for i in coins:
    dfs[f'{i}_target'] = dfs[f'{i}_open'] + (dfs[f'{i}_range'] * k)

for i in coins:
    dfs[f'{i}_ma5'] = dfs[f'{i}_open'].rolling(window=5).mean()

for i in coins:
    dfs[f'{i}_h>t'] = np.where(dfs[f'{i}_high'] > dfs[f'{i}_target'], 1, 0)

for i in coins:
    dfs[f'{i}_o>m'] = np.where(dfs[f'{i}_open'] > dfs[f'{i}_ma5'], 1, 0)

for i in coins:
    dfs[f'{i}_signal'] = dfs[f'{i}_o>m'] * dfs[f'{i}_h>t']

for i in coins:
    dfs[f'{i}_percent'] = np.where(
        target_v > dfs[f'{i}_range_r'], (1/4), (1/4) * (target_v/dfs[f'{i}_range_r']))

for i in coins:
    dfs[f'{i}_R'] = (dfs[f'{i}_close'] * (1-slpy)) / \
        (dfs[f'{i}_target'] * (1+slpy)) - 1


dfs['P_R'] = dfs['btc_R'] * dfs['btc_signal'] * dfs['btc_percent'] + dfs['eth_R'] * dfs['eth_signal'] * dfs['eth_percent'] + dfs['xrp_R'] * \
    dfs['xrp_signal'] * dfs['xrp_percent'] + dfs['ltc_R'] * dfs['ltc_signal'] * \
    dfs['ltc_percent']

length = len(dfs)
dfs.at[dfs.index[0], 'P_B'] = 1
for i in range(1, length):
    dfs.at[dfs.index[i], 'P_B'] = dfs['P_B'][i-1] * (1 + dfs['P_R'][i])

dfs['MDD'] = dfs['P_B']/dfs['P_B'].cummax() -1

s = dfs['P_B'][length - 1]
cagr = s ** (1/(length/365)) - 1
mdd = dfs['MDD'].min()

dfs.at[dfs.index[0], 'result_1'] = '수익률'
dfs.at[dfs.index[1], 'result_1'] = 'CAGR'
dfs.at[dfs.index[2], 'result_1'] = 'MDD'

dfs.at[dfs.index[0], 'result_2'] = s
dfs.at[dfs.index[1], 'result_2'] = cagr
dfs.at[dfs.index[2], 'result_2'] = mdd

print(s)
print(cagr)
print(mdd)

# print(dfs)
# dfs.to_excel("prac2.xlsx")
