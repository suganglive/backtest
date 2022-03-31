import pyupbit
import pandas as pd
import pyupbase as pb
import time

### 모든 tickers 기본 정보 구하기 ###
tickers = pyupbit.get_tickers("KRW")
# hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
hours = ['3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
# windows = [3, 5, 7, 9]
dct = {}


for h in hours:
    df = pd.DataFrame()
    for i in tickers:
        try:
            dct[i] = pb.get_daily_ohlcv_from_base(i, base=h)
            dct[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close", f"{i}_vol"]
            vol1 = dct[i][f"{i}_vol"].rolling(window=5).mean()
            close = dct[i][f"{i}_close"].rolling(window=5).mean()
            dct[i][f"{i}_vol"] = vol1 * close
            dct[i][f"{i}_vol"] = dct[i][f"{i}_vol"].shift(1)
            df = pd.concat([df, dct[i]], axis=1)
        except Exception as e:
            print(i, ' error :', str(e))

    ### 각 rank 정하기, 실행 여부 파악 ###
    df2 = pd.DataFrame.copy(df)
    for i in tickers:
        del df2[f'{i}_open'], df2[f'{i}_high'], df2[f'{i}_low'], df2[f'{i}_close']

    df2.columns = tickers
    df2 = df2.rank(method='min', ascending=False, axis=1)
    df = pd.concat([df, df2], axis=1)

    df.to_excel(f'/Users/sugang/Documents/GitHub/backtest/220326/data_{h}.xlsx')
    print(f'{h} done')
