"""
@file stock.py
@desc: 获取价格，计算涨跌幅
"""

import sys
sys.path.append("D:/pythonCoding/f-quant")

import data.stock as st

code = '000001.XSHE'

# 本地读取数据
data = st.get_csv_price(code,'2025-01-21','2025-02-11')
print(data)
exit()

# 获取行情数据（日K）
data = st.get_single_price(code,'daily','2024-01-01','2024-02-01')
# print(data)

# 计算涨跌幅
# data = st.caculate_change_pct(data)
# print(data)

# 获取周K
data = st.transfer_price_freq(data, 'w')
print(data)

# 计算涨跌幅
data = st.caculate_change_pct(data)
print(data)