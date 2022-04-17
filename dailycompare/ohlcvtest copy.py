import pyupbit
import pandas as pd
import numpy as np
import ranking as rkg
import math

### 기본 자료 불러오기 ###
tickers = pyupbit.get_tickers("KRW")

### 백테스트 ###
k = 0.5
target_v = 0.2
ma = 10
slpy = 0.002
am = 20

def buyable(ticker):
    price = ticker
    # price = price * 1.002
    if price - 1 < 0:
        if price * 10 - 1 < 0:
            price = price * 10000
            if price != int(price):
                price = price + 1
            price = math.floor(price)
            price = price / 10000
        else:
            price = price * 1000
            price = math.floor(price)
            price = price + 1
            price = price / 1000
    elif len(str(math.floor(price))) == 1:
        price = price * 100
        price = math.floor(price)
        price = price + 1
        price = price / 100
    elif len(str(math.floor(price))) == 2:
        price = price * 10
        price = math.floor(price)
        price = price + 1
        price = price / 10
    elif len(str(math.floor(price))) == 3:
        price = math.floor(price)
        price = price + 1
    elif len(str(math.floor(price))) == 4:
        if price % 10 <= 5: 
            price = price / 10
            price = math.floor(price)
            price = price * 10
            price = price + 5
        else:
            price = price / 10
            price = math.floor(price)
            price = price * 10
            price = price + 10
    elif len(str(math.floor(price))) == 5:
        price = price / 10
        price = math.floor(price)
        price = price + 1
        price = price * 10
    elif len(str(math.floor(price))) == 6:
        if (price/10) % 10 <= 5: 
            price = price / 100
            price = math.floor(price)
            price = price * 100
            price = price + 50
        else:
            price = price / 100
            price = math.floor(price)
            price = price * 100
            price = price + 100
    elif len(str(math.floor(price))) >=7:
            price = price / 1000
            price = math.floor(price)
            price = price * 1000
            price = price + 1000
    return price

def hihi(k=0.5, target_v = 0.2, am = 20, m = 10):

    length = len(df)

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
        for j in range(1, length):
            if df.at[df.index[j], f'{i}_target'] <= 500:
                df.at[df.index[j], f'{i}_target'] = buyable(df.at[df.index[j], f'{i}_target'])

    for i in tickers:
        df[f'{i}_ma_n'] = df[f'{i}_open'].rolling(window=m).mean()

    for i in tickers:
        df[f'{i}_h>=t'] = np.where(df[f'{i}_high'] >= df[f'{i}_target'], 1, 0)

    for i in tickers:
        df[f'{i}_o>m'] = np.where(df[f'{i}_open'] > df[f'{i}_ma_n'], 1, 0)

    for i in tickers:
        df[f'{i}_Signal'] = df[f'{i}_o>m'] * df[f'{i}_h>=t'] * df[f'{i}_1/0']

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
    
    df.to_excel("/Users/sugang/Documents/GitHub/backtest/dailycompare/today2.xlsx")
    return s, cagr, mdd

df = rkg.get_rank()
hihi(k,target_v,am,ma)
