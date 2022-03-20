import pyupbit
import pandas as pd
import pyupbase as pb
import time

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
        # vol1 = dct[i][f"{i}_vol"]
        # close = dct[i][f"{i}_close"]
        dct[i][f"{i}_vol"] = vol1 * close
        # dct[i][f"{i}_vol"] = dct[i][f"{i}_vol"].shift(1)
        dct[i][f"{i}_vol"] = dct[i][f"{i}_vol"]
        df = pd.concat([df, dct[i]], axis=1)
        # time.sleep(0.5)
    except Exception as e:
        print(i, ' error :', str(e))

df.to_excel('/Users/sugang/Documents/GitHub/backtest/220319/test0319.xlsx')
