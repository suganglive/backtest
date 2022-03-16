import pyupbit
import pandas as pd
import pyupbase as pb

### 모든 tickers 기본 정보 구하기 ###
tickers = pyupbit.get_tickers("KRW")
# tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-LTC']
dct = {}
hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
for h in hours:
    df = pd.DataFrame()
    for i in tickers:
        try:
            dct[i] = pb.get_daily_ohlcv_from_base(i, base = h)
            dct[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close", f"{i}_vol"]
            vol1 = dct[i][f"{i}_vol"].rolling(window=5).mean()
            close = dct[i][f"{i}_close"].rolling(window=5).mean()
            vol2 = vol1 * close
            dct[i][f"{i}_vol"] = vol2
            df = pd.concat([df, dct[i]], axis=1)
        except Exception as e:
            print(i, ' error :', str(e))

    df.to_excel(f'/Users/sugang/Documents/GitHub/backtest/alldata1y/{h}_all.xlsx')
    print(h, 'done')