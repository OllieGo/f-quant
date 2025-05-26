"""
@file momentum_strategy.py
@desc: 动量策略（正向）
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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
双均线策略
param: data: dataframe, 投资标的行情数据（必须包含收盘价）
param: short_window:短期n日移动平均线,默认5
param: long_window:长期n日移动平均线,默认20
return: 
"""

def get_data(index_symbol='000300.XSHG'):
    # 获取股票列表代码:沪深300持有个股、创业板、上证
    stocks = st.get_index_list(index_symbol)
    
    # 获取股票数据
    for code in stocks:
        data = st.get_csv_price(code, '2024-02-22', '2025-02-22')
        # 预览股票数据
        print("=========", code)
        print(data.tail())

def momentum():
    return 0
    
if __name__ == '__main__':
    get_data()