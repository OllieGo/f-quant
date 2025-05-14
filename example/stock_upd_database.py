"""
@file stock_database.py
@desc: 用于调用股票行情数据的脚本
"""

import sys
sys.path.append("D:/pythonCoding/f-quant")


import data.stock as st
import pandas as pd

# 初始化变量
code='000002.XSHE'

# 调用一只股票的行情数据
# data = st.get_single_price(code=code,
#                            time_freq = 'daily',
#                            start_date = '2024-02-01',
#                            end_date = '2024-07-01')

# 存入csv
# st.export_data(data=data, filename=code, type='price')

# 从csv中获取数据
# data = st.get_csv_data(code=code, type='price')
# print(data)

# 实时更新数据：假设每天更新 > 存到csv文件里面

# 1.获取所有股票代码
# stocks = st.get_stock_list()
# 2.存储到scv中
# for code in stocks:
#     df = st.get_single_price(code, 'daily')
#     st.export_data(df)
st.init_db()

# 3.每日更新数据：
# for code in stocks:
#     st.update_daily_price(code, 'price')


