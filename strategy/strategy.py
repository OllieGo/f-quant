"""
@file strategy.py
@desc: 创建交易策略、生成交易信号
"""

import sys
sys.path.append("D:/pythonCoding/f-quant")

import data.stock as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
整合信号
param: data
return: 
"""
def compose_singal(data):
    data['buy_signal'] = np.where((data['buy_signal'] == 1) 
        & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) 
        & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])

    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

"""
计算单次收益率：开仓、平仓（开仓的全部股数）
param: data
return: 
"""
def caculate_prof_pct(data):
    data = data[data['signal'] != 0] # 筛选
 
    # 确保data不是一个视图，而是一个独立的DataFrame对象
    data = data.copy()
    data.loc[:, 'profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)

    data = data[data['signal'] == -1]
    return data


def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入 1买入 0无操作 -1卖出
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    # 整合信号
    data = compose_singal(data)

    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    data = caculate_prof_pct(data)

    return data

if __name__ == '__main__':
    code = '000001.XSHE'
    # data = week_period_strategy(code, 'daily', '2024-01-01', '2024-03-01')
    df = week_period_strategy(code, 'daily', None, '2025-01-07')
    # print(data[['close', 'weekday', 'buy_signal', 'sell_signal', 'signal']])
    print(df[['close', 'signal', 'profit_pct']])
    print(df.describe())
    df['profit_pct'].plot()
    plt.show()

