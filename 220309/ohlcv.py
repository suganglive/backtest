import pyupbit
import pandas as pd
import numpy as np

# import logging

# logging.basicConfig(filename='upbit8.log', level=logging.INFO, format='%(created)f:%(message)s')

tickers = pyupbit.get_tickers("KRW")
# tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP']
dct2 = {}
dct = {}
df = pd.DataFrame()
for ticker in tickers:
    try:
        dct[ticker] = pyupbit.get_ohlcv(ticker, interval='day', count=365)
        del dct[ticker]['value']
        dct[ticker].columns = [f"{ticker}_open", f"{ticker}_high", f"{ticker}_low", f"{ticker}_close", f"{ticker}_volume"]
        vol1 = dct[ticker][f"{ticker}_volume"].rolling(window=5).mean()
        close = dct[ticker][f"{ticker}_close"].rolling(window=5).mean()
        vol2 = vol1 * close
        dct[ticker][f"{ticker}_volume"] = vol2
        df = pd.concat([df, dct[ticker]], axis=1)
    except Exception as e:
        print(ticker, ' error :', str(e))
# df.to_excel("220309.xlsx")

df2 = pd.DataFrame.copy(df)
# print(df)
for ticker in tickers:
    del df2[f'{ticker}_open'], df2[f'{ticker}_high'], df2[f'{ticker}_low'], df2[f'{ticker}_close']

df2.columns = tickers
df2 = df2.rank(method='min', ascending=False, axis=1)

df = pd.concat([df, df2], axis=1)

for ticker in tickers:
    df[f'{ticker}_1/0'] = np.where(df[f'{ticker}'] <= 5, 1, 0)

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
        df[f'{i}_signal'] = df[f'{i}_o>m'] * df[f'{i}_h>t']

    for i in tickers:
        df[f'{i}_percent'] = np.where(
            target_v > df[f'{i}_range_r'], (1/amount), (1/amount) * (target_v/df[f'{i}_range_r']))

    for i in tickers:
        df[f'{i}_R'] = (df[f'{i}_close'] * (1-slpy)) / \
            (df[f'{i}_target'] * (1+slpy)) - 1

    for i in tickers:
        df[f'{i}_R_2'] = df[f'{i}_R'] * df[f'{i}_signal'] * df[f'{i}_percent'] * df[f'{i}_1/0']
    
    df['R'] = 0
    
    for i in tickers:
        df['R'] = df['R'] + df[f'{i}_R_2']
        
#     length = len(df)

#     dict = {}
#     for i in tickers:
#         dict[i] = df[f'{i}_R'] * df[f'{i}_signal'] * df[f'{i}_percent'] * df[f'{i}_1/0']
    
#     for i in tickers:
#         # df['P_R'] = df['P_R'] + dict[i] 

#     df.at[df.index[0], 'P_B'] = 1
#     for i in range(1, length):
#         df.at[df.index[i], 'P_B'] = df['P_B'][i-1] * (1 + df['P_R'][i])

#     df['MDD'] = df['P_B']/df['P_B'].cummax() -1

#     s = df['P_B'][length - 1]
#     cagr = s ** (1/(length/365)) - 1
#     mdd = df['MDD'].min()

#     df.at[df.index[0], 'result_1'] = '수익률'
#     df.at[df.index[1], 'result_1'] = 'CAGR'
#     df.at[df.index[2], 'result_1'] = 'MDD'

#     df.at[df.index[0], 'result_2'] = s
#     df.at[df.index[1], 'result_2'] = cagr
#     df.at[df.index[2], 'result_2'] = mdd
    
    df.to_excel("joke1.xlsx")
#     return s, cagr, mdd

df = hihi()

# df.to_excel("220309.xlsx")