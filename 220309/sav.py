import pyupbit

tickers = pyupbit.get_tickers("KRW")
dct = {}
winners = []

for tick in tickers:
        data = pyupbit.get_ohlcv(tick, count=365)
        try:
            vol1 = data['volume'].rolling(window=5).mean()
            close = data['close'].rolling(window=5).mean()
            vol2 = vol1 * close
            dct[tick] = vol2[-1]
        except:
            print(f"{tick}_error")

sorted_d = dict(sorted(dct.items(), key=operator.itemgetter(1), reverse=True))
print("Dictionay in descending order by value : ", sorted_d)