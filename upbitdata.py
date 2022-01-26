import pyupbit

tkrs = pyupbit.get_tickers(fiat='KRW')

current_prices = pyupbit.get_current_price(["KRW-BTC", "KRW-ETH"])

ticker = 'KRW-BTC'
interval = 'day'
to = '2022-01-27'
count = 10

a = pyupbit.get_ohlcv(ticker=ticker, interval=interval, to=to, count = count)

print(a)
