import pyupbit
import pandas as pd
import numpy as np
import pyupbase as pb

### 모든 tickers 기본 정보 구하기 ###
tickers = pyupbit.get_tickers("KRW")
# tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-LTC']
dct = {}
df = pd.DataFrame()
for i in tickers:
    try:
        dct[i] = pb.get_daily_ohlcv_from_base(i)
        dct[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close", f"{i}_vol"]
        vol1 = dct[i][f"{i}_vol"].rolling(window=5).mean()
        close = dct[i][f"{i}_close"].rolling(window=5).mean()
        length = dct[i]
        vol2 = vol1 * close
        dct[i][f"{i}_vol"] = vol2
        df = pd.concat([df, dct[i]], axis=1)
    except Exception as e:
        print(i, ' error :', str(e))

df.to_excel('10h_all.xlsx')

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
amount = 4
dct2 = {}

def hihi(k=0.5, target_v = 0.05):
    for i in tickers:
        dct2[f'{i}_range'] = df[f'{i}_high'] - df[f'{i}_low']
        dct2[f'{i}_range'] = dct2[f'{i}_range'].shift(1)

    for i in tickers:
        dct2[f'{i}_range_r'] = (dct2[f'{i}_range'].shift(-1))/(df[f'{i}_open'])
        dct2[f'{i}_range_r'] = dct2[f'{i}_range_r'].shift(1)

    for i in tickers:
        dct2[f'{i}_target'] = df[f'{i}_open'] + (dct2[f'{i}_range'] * k)

    for i in tickers:
        dct2[f'{i}_ma5'] = df[f'{i}_open'].rolling(window=5).mean()

    for i in tickers:
        dct2[f'{i}_h>t'] = np.where(df[f'{i}_high'] > dct2[f'{i}_target'], 1, 0)

    for i in tickers:
        dct2[f'{i}_o>m'] = np.where(df[f'{i}_open'] > dct2[f'{i}_ma5'], 1, 0)

    for i in tickers:
        df[f'{i}_signal'] = dct2[f'{i}_o>m'] * dct2[f'{i}_h>t'] * df[f'{i}_1/0']

    for i in tickers:
        df[f'{i}_percent'] = np.where(
            target_v > dct2[f'{i}_range_r'], (1/amount), (1/amount) * (target_v/dct2[f'{i}_range_r']))

    for i in tickers:
        df[f'{i}_R'] = (df[f'{i}_close'] * (1-slpy)) / \
            (dct2[f'{i}_target'] * (1+slpy)) - 1

    for i in tickers:
        df[f'{i}_R_2'] = df[f'{i}_R'] * df[f'{i}_signal'] * df[f'{i}_percent']
    
    df['P_R'] = 0
    for i in tickers:
        df['P_R'] = df['P_R'] + df[f'{i}_R_2']

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
    df.to_excel("joke5.xlsx")
    return s, cagr, mdd

a = hihi()
print(a)

