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
def calculate_prof_pct(data):
    # 筛选信号不为0的 ，并且计算涨跌幅
    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
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
    data = calculate_prof_pct(data)

    # 计算累计收益率
    data = calculate_cum_prof(data)

    # 最大回撤
    data = calculate_max_drawdown(data)
    
    return data

if __name__ == '__main__':
    code = '000001.XSHE'
    # data = week_period_strategy(code, 'daily', '2024-01-01', '2024-03-01')
    # df = week_period_strategy(code, 'daily', None, '2025-01-07')
    # print(data[['close', 'weekday', 'buy_signal', 'sell_signal', 'signal']])
    # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    # print(df.describe())
    # df['cum_profit'].plot()
    # plt.show()

    # 查看最大回撤
    # df = st.get_single_price(code, 'daily', None, '2025-01-07')
    # df = calculate_max_drawdown(df)
    # print(df[['close', 'roll_max', 'daily_dd', 'max_dd']])
    # df[['daily_dd', 'max_dd']].plot()
    # plt.show()

    # 计算夏普比率
    df = st.get_single_price(code, 'daily', None, '2025-01-07')
    sharpe = calculate_sharpe(df)
    print(sharpe)
