import pyupbit
import pandas as pd
import numpy as np
import pyupbase as pb

# logging.basicConfig(filename='10h_k_v_am_m.log', level=logging.INFO, format='%(message)s')

# hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
# hours = '10h'
# ks = np.arange(0.1, 1.1, 0.1)
# ks = [0.5, 0.8]
# vs = np.arange(0.01, 0.5, 0.01)
# vs = [0.01, 0.03, 0.05, 0.1, 0.2]
# amount = range(1, 21)
# amount = [1, 3, 5, 10, 15, 20, 25, 30]
# ma = range(1, 31)
# ma = [3, 5, 7, 10, 15, 20, 30]


### 기본 자료 불러오기 ###
tickers = pyupbit.get_tickers("KRW")
df = pd.read_excel('/Users/sugang/Documents/GitHub/backtest/220319/test0322_9h.xlsx', index_col=0)

# ### 각 rank 정하기, 실행 여부 파악 ###
# df2 = pd.DataFrame.copy(df)
# for i in tickers:
#     del df2[f'{i}_open'], df2[f'{i}_high'], df2[f'{i}_low'], df2[f'{i}_close']

# df2.columns = tickers
# df2 = df2.rank(method='min', ascending=False, axis=1)
# df = pd.concat([df, df2], axis=1)

# for i in tickers:
#     df[f'{i}_1/0'] = np.where(df[f'{i}'] <= 5, 1, 0)

### 백테스트 ###
# k = 0.8
# target_v = 0.2
slpy = 0.002
# amount = 15
# amount = 10
# amount = 15

def hihi(k=0.8, target_v = 0.2, am = 15, m = 5):
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
    
    df.to_excel("/Users/sugang/Documents/GitHub/backtest/220319/test0322_9h_1.xlsx")
    return s, cagr, mdd

# for hour in (hours):
#     df = pd.read_excel(f'/Users/sugang/Documents/GitHub/backtest/data/up_{hour}.xlsx')
#     for k in np.arange(0.1, 1, 0.1):
#         for v in np.arange(0.01, 0.2, 0.01):
#             s = hihi(k, v)[0]
#             cagr = hihi(k, v)[1]
#             mdd = hihi(k, v)[2]
#             logging.info(f'{hour}, {k}, {v}, {cagr}, {mdd}')

# df = pd.read_excel('/Users/sugang/Documents/GitHub/backtest/220316/letsgo.xlsx', index_col=0)
# for k in ks:
#     for v in vs:
#         for am in amount:
#             for m in ma:
#                 s = hihi(k=k, target_v=v, am=am, m=m)[0]
#                 cagr = hihi(k=k, target_v=v, am=am, m=m)[1]
#                 mdd = hihi(k=k, target_v=v, am=am, m=m)[2]
#                 logging.info(f'{k}, {v}, {am}, {m}, {cagr}, {mdd}')

hihi()