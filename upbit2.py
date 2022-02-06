import pyupbit
import pandas as pd
import openpyxl


tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-LTC']

df1 = pd.DataFrame()
df1.to_excel("hi1.xlsx")

with pd.ExcelWriter('hi1.xlsx', mode='a') as writer:
    for i in tickers:
        interval = 'day'
        to = '2100-01-01'
        a = pyupbit.get_daily_ohlcv_from_base("KRW-BTC", base=1)
        a.to_excel(writer, sheet_name=i)
