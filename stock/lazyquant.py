#필요 라이브러리 import
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import math
import quantstats as qs

# pandas 설정 및 메타데이터 세팅
pd.options.display.float_format = '{:.4f}'.format
pd.set_option('display.max_columns', None)

start_day = datetime(2008,1,1) # 시작일
end_day = datetime(2021,11,30) # 종료일

# RU = Risky Universe
# CU = Cash Universe
# BU = Benchmark Universe
RU = ['SPY', 'VEA', 'EEM', 'AGG']
CU = ['LQD', 'SHY', 'IEF']
BU = ['^GSPC', '^IXIC', '^KS11', '^KQ11'] # S&P 500, 나스닥, 코스피, 코스닥

def get_price_data(RU, CU, BU):
    df_RCU = pd.DataFrame(columns=RU+CU)
    df_BU = pd.DataFrame(columns=BU)

    for ticker in RU + CU:
        df_RCU[ticker] = pdr.get_data_yahoo(ticker, start_day - timedelta(days=365), end_day)['Adj Close']
    
    for ticker in BU:
        df_BU[ticker] = pdr.get_data_yahoo(ticker, start_day - timedelta(days=365), end_day)['Adj Close']

    return df_RCU, df_BU

# 각 자산군의 데이터 추출
df_RCU, df_BU = get_price_data(RU, CU, BU)

# 모멘텀 지수 계산 함수
def get_momentum(x):
    temp_list = [0 for i in range(len(x.index))]
    momentum = pd.Series(temp_list, index=x.index)

    try:
        before1 = df_RCU[x.name-timedelta(days=35):x.name-timedelta(day=30)].iloc[-1][RU+CU]
        before3 = df_RCU[x.name-timedelta(days=95):x.name-timedelta(day=90)].iloc[-1][RU+CU]
        before6 = df_RCU[x.name-timedelta(days=185):x.name-timedelta(day=180)].iloc[-1][RU+CU]
        before12 = df_RCU[x.name-timedelta(days=370):x.name-timedelta(day=365)].iloc[-1][RU+CU]

        momentum = 12 * (x / before1 - 1) + 4 * (x / before3 - 1) + 2 * (x / before6 - 1) + (x / before12 - 1) 
    except Exception as e:
        print("Error : ", str(e))
        pass
    
    return momentum
    #     momentum = 12 * (x / before1 - 1) + 4 * (x / before3 - 1) + 2 * (x / before6 - 1) + (x / before12 - 1)
    # except Exception as e:
    #     #print("Error : ", str(e))
    #     pass

    # return momentum

# 각 자산별 모멘텀 지수 계산
mom_col_list = [col+'_M' for col in df_RCU[RU+CU].columns]
df_RCU[mom_col_list] = df_RCU[RU+CU].apply(lambda x: get_momentum(x), axis=1)

# 백테스트할 기간 데이터 추출
df_RCU = df_RCU[start_day:end_day]

# 매월 말일 데이터만 추출
df_RCU = df_RCU.resample(rule='M').last()

