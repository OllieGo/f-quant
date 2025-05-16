"""
@file statistical_test.py
@desc: 双均线策略
"""

import sys
import os


# 获取当前脚本所在目录（即 strategy 文件夹）
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录 f-quant
project_root = os.path.dirname(current_dir)

# 将项目根目录加入系统路径
if project_root not in sys.path:
    sys.path.append(project_root)

import data.stock as st
import strategy.ma_strategy as ma
import matplotlib.pyplot as plt
from scipy import stats

"""
对策略收益进行t检验
param: strat_return: dataframe,单次收益率
return: float,t值和p值
"""
def ttest(data_return):

    # 调用假设检验ttest函数：scipy
    t, p = stats.ttest_1samp(data_return, 0, nan_policy='omit')

    # 判断是否与理论均值有显著差异:α=0.05
    p_value = p / 2 # 获取单边p值

    # 打印
    print("t_value:", t)
    print("p_value:", p_value)
    print("是否可以拒绝[H0]收益均值 = 0:", p_value < 0.05)

    return t, p_value


if __name__ == '__main__':
    stocks = ['000001.XSHE','000858.XSHE','002594.XSHE']
    for code in stocks:
        print(code)
        df = st.get_single_price(code, 'daily', '2024-02-06', '2025-02-12')
        df = ma.ma_strategy(df) # 调用双均线策略

        # 策略单次收益率
        returns = df['profit_pct']
        # print(returns)
        
        # 绘制分布图用于观察
        # plt.hist(returns)
        # plt.show()

        # 对多个股票进行计算、测试
        ttest(returns)

    