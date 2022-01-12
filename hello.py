import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta
import backtrader as bt
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
import pyfolio as pf
import quantstats
import math
import seaborn
plt.rcParams["figure.figsize"] = (10, 6) # (w, h)

# 공격 자산: SPY (S&P 500), EFA (MSCI EAFE), EEM (Emerging), AGG (Aggregate US Bond) 
# 방어 자산: LQD (Investment Grade Corporate Bond), IEF (US 7-10 Year Treausry), SHY (US 1-3 Year Treasury)

# AGG starts: 2003-09-29
start = datetime(2003,10,1)
end = datetime(2021,5,31)

tickers = ['SPY','EFA','EEM','AGG','LQD','SHY','IEF']

def get_price_data(tickers):
    df_asset = pd.DataFrame(columns=tickers)
    
    for ticker in tickers:
        df_asset[ticker] = pdr.get_data_yahoo(ticker, start, end)['Adj Close']  
         
    return df_asset

df_asset = get_price_data(tickers)
df_asset