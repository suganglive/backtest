import numpy as np
import pandas as pd
import datetime

def get_daily_ohlcv_from_base(ticker = "hi", base=0):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        df = pd.read_excel(f"/Users/sugang/Documents/GitHub/backtest/binancedata/bi_{ticker}_long.xlsx", index_col=0)
        df.index = df.index + datetime.timedelta(hours=9)
        df = df.resample('24H', offset=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        return df
    except Exception as x:
        return None

hours = ['1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '0h']
for hour in hours:
    ss = {'btc': get_daily_ohlcv_from_base(ticker="btc", base = hour), 'eth': get_daily_ohlcv_from_base(ticker="eth", base = hour),
        'xrp': get_daily_ohlcv_from_base(ticker="xrp", base = hour), 'ltc': get_daily_ohlcv_from_base(ticker="ltc", base = hour)}

    for i in ss:
        ss[i].columns = [f"{i}_open", f"{i}_high", f"{i}_low", f"{i}_close"]

    dfs = pd.concat([ss['btc'], ss['eth'], ss['xrp'], ss['ltc']], axis=1)

    dfs = dfs[['btc_open', 'eth_open', 'xrp_open', 'ltc_open', 'btc_high', 'eth_high', 'xrp_high', 'ltc_high',
                'btc_low', 'eth_low', 'xrp_low', 'ltc_low', 'btc_close', 'eth_close', 'xrp_close', 'ltc_close']]

    dfs.to_excel(f'/Users/sugang/Documents/GitHub/backtest/binancedata/bi_{hour}_timeadj.xlsx')

    # dfs = pd.read_excel(f'/Users/sugang/Documents/GitHub/backtest/data/{hour}.xlsx')

    # dfs = dfs.drop(range(0, 8))

    # dfs.to_excel(f'/Users/sugang/Documents/GitHub/backtest/data/{hour}.xlsx')
    print(f'{hour}-done')
