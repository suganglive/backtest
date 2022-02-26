from operator import index
import pyupbit
import numpy as np
import pandas as pd
import logging
import datetime

hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
k = 0.5
coins = ['btc', 'eth', 'xrp', 'ltc']
target_v = 0.05
slpy = 0.002

# def get_daily_ohlcv_from_base(ticker="KRW-BTC", base=0):
#     """
#     :param ticker:
#     :param base:
#     :return:
#     """
#     try:
#         # df = pyupbit.get_ohlcv(ticker, interval="minute60", count=37898)
#         # df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=13737)
#         df = pyupbit.get_ohlcv(ticker, interval="minute60", count=240)
#         df = df.resample('24H', offset=base).agg(
#             {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
#         return df
#     except Exception as x:
#         return None

def hihi(k=0.5, target_v = 0.05):
    for i in coins:
        df[f'{i}_range'] = df[f'{i}_high'] - df[f'{i}_low']
        df[f'{i}_range'] = df[f'{i}_range'].shift(1)

    for i in coins:
        df[f'{i}_range_r'] = (df[f'{i}_range'].shift(-1))/(df[f'{i}_open'])
        df[f'{i}_range_r'] = df[f'{i}_range_r'].shift(1)

    for i in coins:
        df[f'{i}_target'] = df[f'{i}_open'] + (df[f'{i}_range'] * k)

    for i in coins:
        df[f'{i}_ma5'] = df[f'{i}_open'].rolling(window=5).mean()

    for i in coins:
        df[f'{i}_h>t'] = np.where(df[f'{i}_high'] > df[f'{i}_target'], 1, 0)

    for i in coins:
        df[f'{i}_o>m'] = np.where(df[f'{i}_open'] > df[f'{i}_ma5'], 1, 0)

    for i in coins:
        df[f'{i}_signal'] = df[f'{i}_o>m'] * df[f'{i}_h>t']

    for i in coins:
        df[f'{i}_percent'] = np.where(
            target_v > df[f'{i}_range_r'], (1/4), (1/4) * (target_v/df[f'{i}_range_r']))

    for i in coins:
        df[f'{i}_R'] = (df[f'{i}_close'] * (1-slpy)) / \
            (df[f'{i}_target'] * (1+slpy)) - 1


    df[f'{hour}_P_R'] = df['btc_R'] * df['btc_signal'] * df['btc_percent'] + df['eth_R'] * df['eth_signal'] * df['eth_percent'] + df['xrp_R'] * \
        df['xrp_signal'] * df['xrp_percent'] + df['ltc_R'] * df['ltc_signal'] * \
        df['ltc_percent']

    length = len(df)
    df.at[df.index[0], f'{hour}_P_B'] = 1
    for i in range(1, length):
        df.at[df.index[i], f'{hour}_P_B'] = df[f'{hour}_P_B'][i-1] * (1 + df[f'{hour}_P_R'][i])

    df[f'{hour}_MDD'] = df[f'{hour}_P_B']/df[f'{hour}_P_B'].cummax() -1

    # s = df['P_B'][length - 1]
    # cagr = s ** (1/(length/365)) - 1
    # mdd = df['MDD'].min()

    # df.at[df.index[0], 'result_1'] = '수익률'
    # df.at[df.index[1], 'result_1'] = 'CAGR'
    # df.at[df.index[2], 'result_1'] = 'MDD'

    # df.at[df.index[0], 'result_2'] = s
    # df.at[df.index[1], 'result_2'] = cagr
    # df.at[df.index[2], 'result_2'] = mdd

    return df[f'{hour}_P_R'], df[f'{hour}_P_B'], df[f'{hour}_MDD']

h1 = 0
h2 = 0
h3 = 0
h4 = 0
h5 = 0
h6 = 0
h7 = 0
h8 = 0
h9 = 0
h10 = 0
h11 = 0
h12 = 0
h13 = 0
h14 = 0
h15 = 0
h16 = 0
h17 = 0
h18 = 0
h19 = 0
h20 = 0
h21 = 0
h22 = 0
h23 = 0
h0 = 0

# kimchi = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, h0]
# gogi = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]
# ran = range(0, 574)
for i, hour in enumerate(hours):
    df = pd.read_excel(f"/Users/sugang/Documents/GitHub/backtest/data/{hour}.xlsx", index_col=0)
    # df.index = pd.to_datetime(df.index)
    kimchi[i] = pd.concat([hihi()[0], hihi()[1], hihi()[2]], axis=1)
    print(kimchi[i])

# zz = pd.concat(kimchi, axis=1)
# zz.to_excel("hour_momentum.xlsx")

