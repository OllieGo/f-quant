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
def compose_signal(data):
     # 对于连续的买入信号，仅保留第一个
    data['buy_signal'] = np.where((data['buy_signal'] == 1) 
        & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    
    # 对于连续的卖出信号，仅保留第一个
    data['sell_signal'] = np.where((data['sell_signal'] == -1) 
        & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])

    # 整合买入和卖出信号
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

"""
计算单次收益率：开仓、平仓（开仓的全部股数）
param: data
return: 
"""
def calculate_prof_pct(data):
    # 筛选信号不为0的 ，并且计算涨跌幅
    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
    # 筛选平仓后数据：单次收益
    data = data[data['signal'] == -1]
    return data

"""
计算累计收益率
param data: dataFrame
return: 
"""
def calculate_cum_prof(data):
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data

"""
计算最大回撤比
param: data
return: 
"""
def calculate_max_drawdown(data):
    # 选取时间周期
    window = 252
    # 计算时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window,min_periods=1).max()
    # 计算当天的回撤比 （谷值-峰值）/ 峰值 = 谷值 / 峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内的最大回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window=252,min_periods=1).min()
   
    return data

"""
计算夏普比率，返回年华夏普比率
param: data: dataframe,stock
return: float
"""
def calculate_sharpe(data):
    # 公式: sharpe = （回报率的均值 - 无风险利率） / 回报率的标准差
    # 因子项
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普：每日收益 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year

