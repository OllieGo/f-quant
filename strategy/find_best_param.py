"""
@file find_best_param.py
@desc: 寻找最优参数(以MA双均线策略为例)
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

import strategy.ma_strategy as ma
import data.stock as st
import pandas as pd


# 参数1：股票池
# stocks = ['000001.XSHE']
code = '000001.XSHE'
data = st.get_csv_price(code, '2024-02-05', '2025-02-15')

# 参数2：周期参数
params = [5, 10, 20, 60, 120, 250]

# 存放参数与收益
res = []

# 匹配并计算不同的周期参数对： 5-10，5-20 ... 120-250
for short in params:
    for long in params:
        if long > short:
            data_res = ma.ma_strategy(data=data, short_window=short, long_window=long)
            # 获取周期参数，及其对应累计收益率

            # 检查data_res是否为空
            if not data_res.empty and 'cum_profit' in data_res.columns:
                cum_profit = data_res['cum_profit'].iloc[-1]  # 获取累计收益率最终数据
                res.append([short, long, cum_profit])  # 将参数放入结果列表
            else:
                print(f"No data or missing 'cum_profit' column for short={short}, long={long}")

# 将结果列表转换为df，并找到最优参数
res = pd.DataFrame(res, columns=['short_win','long_win','cum_profit'])
# 排序
res = res.sort_values(by='cum_profit', ascending=False) # 按收益倒序排列

print(res)
