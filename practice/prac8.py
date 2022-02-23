#10h 0.8k 0.19v
import pyupbit
import numpy as np
import pandas as pd
import datetime
import logging

logging.basicConfig(filename='prac7.log', level=logging.INFO, format='%(message)s')
hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']

k = 0.5
coins = ['btc', 'eth', 'xrp', 'ltc']
target_v = 0.05
slpy = 0.002

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


    df['P_R'] = df['btc_R'] * df['btc_signal'] * df['btc_percent'] + df['eth_R'] * df['eth_signal'] * df['eth_percent'] + df['xrp_R'] * \
        df['xrp_signal'] * df['xrp_percent'] + df['ltc_R'] * df['ltc_signal'] * \
        df['ltc_percent']

    length = len(df)
    df.at[df.index[0], 'P_B'] = 1
    for i in range(1, length):
        df.at[df.index[i], 'P_B'] = df['P_B'][i-1] * (1 + df['P_R'][i])

    df['MDD'] = df['P_B']/df['P_B'].cummax() -1

    s = df['P_B'][length - 1]
    cagr = s ** (1/(length/365)) - 1
    mdd = df['MDD'].min()

    df.at[df.index[0], 'result_1'] = '수익률'
    df.at[df.index[1], 'result_1'] = 'CAGR'
    df.at[df.index[2], 'result_1'] = 'MDD'

    df.at[df.index[0], 'result_2'] = s
    df.at[df.index[1], 'result_2'] = cagr
    df.at[df.index[2], 'result_2'] = mdd
    
    df.to_excel("11h_0.5k_0.05v.xlsx")
    return s, cagr, mdd

df = pd.read_excel(f'/Users/sugang/Documents/GitHub/backtest/data/11h.xlsx')
hihi(k=0.5, target_v=0.05)