import pyupbit
import pandas as pd
import numpy as np
import ranking as rkg

### 기본 자료 불러오기 ###
tickers = pyupbit.get_tickers("KRW")

### 백테스트 ###
k = 0.8
target_v = 0.2
ma = 10
slpy = 0.002
am = 20

def hihi(k=0.5, target_v = 0.2, am = 20, m = 10):
    for i in tickers:
        df[f'{i}_1/0'] = np.where(df[f'{i}'] <= am, 1, 0)

    for i in tickers:
        df[f'{i}_range'] = df[f'{i}_high'] - df[f'{i}_low']
        df[f'{i}_range'] = df[f'{i}_range'].shift(1)

    for i in tickers:
        df[f'{i}_range_r'] = (df[f'{i}_range'].shift(-1))/(df[f'{i}_open'])
        df[f'{i}_range_r'] = df[f'{i}_range_r'].shift(1)

    for i in tickers:
        df[f'{i}_target'] = df[f'{i}_open'] + (df[f'{i}_range'] * k)

    for i in tickers:
        df[f'{i}_ma_n'] = df[f'{i}_open'].rolling(window=m).mean()

    for i in tickers:
        df[f'{i}_h>t'] = np.where(df[f'{i}_high'] > df[f'{i}_target'], 1, 0)

    for i in tickers:
        df[f'{i}_o>m'] = np.where(df[f'{i}_open'] > df[f'{i}_ma_n'], 1, 0)

    for i in tickers:
        df[f'{i}_Signal'] = df[f'{i}_o>m'] * df[f'{i}_h>t'] * df[f'{i}_1/0']

    for i in tickers:
        df[f'{i}_percent'] = np.where(
            target_v > df[f'{i}_range_r'], (1/am), (1/am) * (target_v/df[f'{i}_range_r']))

    for i in tickers:
        df[f'{i}_R'] = (df[f'{i}_close'] * (1-slpy)) / \
            (df[f'{i}_target'] * (1+slpy)) - 1

    df2 = pd.DataFrame()
    for i in tickers:
        df[f'{i}_R_2'] = df[f'{i}_R'] * df[f'{i}_Signal'] * df[f'{i}_percent']
        df2 = pd.concat([df2, df[f'{i}_R_2']], axis=1)
    
    df['P_R'] = df2.sum(axis=1)

    length = len(df)

    df.at[df.index[0], 'P_B'] = 1
    for i in range(1, length):
        df.at[df.index[i], 'P_B'] = df['P_B'][i-1] * (1 + df['P_R'][i])

    df['MDD'] = df['P_B']/df['P_B'].cummax() -1

    s = df['P_B'][length - 1]
    s = s - 1
    cagr = df['P_B'][length - 1] ** (1/(length/365)) - 1
    mdd = df['MDD'].min()

    df.at[df.index[0], 'result_1'] = '수익률'
    df.at[df.index[1], 'result_1'] = 'CAGR'
    df.at[df.index[2], 'result_1'] = 'MDD'

    df.at[df.index[0], 'result_2'] = s
    df.at[df.index[1], 'result_2'] = cagr
    df.at[df.index[2], 'result_2'] = mdd
    
    df.to_excel("/Users/sugang/Documents/GitHub/backtest/dailycompare/today.xlsx")
    return s, cagr, mdd

df = rkg.get_rank()
hihi(k,target_v,am,ma)
