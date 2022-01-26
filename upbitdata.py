import pyupbit
import pandas as pd
import openpyxl


tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-DOGE', 'KRW-LTC']



for i in tickers:

    ticker = i
    interval = 'day'
    to = '2100-01-01'
    a = pyupbit.get_ohlcv(ticker=ticker, interval=interval, to=to, count=3)
    
    with pd.ExcelWriter('practice.xlsx') as writer:
        a.to_excel(writer, sheet_name=i)
    



# path = 'pandas_to_excel.xlsx'

# with pd.ExcelWriter(path) as writer:
#     writer.book = openpyxl.load_workbook(path)
#     df.to_excel(writer, sheet_name='new_sheet1')
#     df2.to_excel(writer, sheet_name='new_sheet2')
