import pyupbit
import pandas as pd
import numpy as np
import pyupbase as pb

### 기본 자료 불러오기 ###
tickers = pyupbit.get_tickers("KRW")
df = pd.read_excel("10h_all.xlsx", index_col=0)

### 각 rank 정하기, 실행 여부 파악 ###
df2 = pd.DataFrame.copy(df)
# print(df)
for i in tickers:
    del df2[f'{i}_open'], df2[f'{i}_high'], df2[f'{i}_low'], df2[f'{i}_close']

df2.columns = tickers
df2 = df2.rank(method='min', ascending=False, axis=1)

df = pd.concat([df, df2], axis=1)

for i in tickers:
    df[f'{i}_1/0'] = np.where(df[f'{i}'] <= 5, 1, 0)

### 백테스트 ###
k = 0.5
target_v = 0.05
slpy = 0.002
amount = 5

def hihi(k=0.5, target_v = 0.05):
    for i in tickers:
        df[f'{i}_range'] = df[f'{i}_high'] - df[f'{i}_low']
        df[f'{i}_range'] = df[f'{i}_range'].shift(1)

    for i in tickers:
        df[f'{i}_range_r'] = (df[f'{i}_range'].shift(-1))/(df[f'{i}_open'])
        df[f'{i}_range_r'] = df[f'{i}_range_r'].shift(1)

    for i in tickers:
        df[f'{i}_target'] = df[f'{i}_open'] + (df[f'{i}_range'] * k)

    for i in tickers:
        df[f'{i}_ma5'] = df[f'{i}_open'].rolling(window=5).mean()

    for i in tickers:
        df[f'{i}_h>t'] = np.where(df[f'{i}_high'] > df[f'{i}_target'], 1, 0)

    for i in tickers:
        df[f'{i}_o>m'] = np.where(df[f'{i}_open'] > df[f'{i}_ma5'], 1, 0)

    for i in tickers:
        df[f'{i}_Signal'] = df[f'{i}_o>m'] * df[f'{i}_h>t'] * df[f'{i}_1/0']

    for i in tickers:
        df[f'{i}_percent'] = np.where(
            target_v > df[f'{i}_range_r'], (1/amount), (1/amount) * (target_v/df[f'{i}_range_r']))

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
    
    df.to_excel("ohlcv4.xlsx")
    return s, cagr, mdd

a = hihi()
print(a)

