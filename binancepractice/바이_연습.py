import pandas as pd
import datetime

df = pd.read_excel("/Users/sugang/Documents/GitHub/backtest/binancedata/bi_23h.xlsx", index_col=0)

df.index = df.index + datetime.timedelta(hours=9)

print(df)