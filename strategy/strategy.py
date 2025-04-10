"""
@file strategy.py
@desc: 创建交易策略、生成交易信号
"""

import sys
sys.path.append("D:/pythonCoding/f-quant")

import data.stock as st
import numpy as np

def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入 1买入 0无操作 -1卖出
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) 
        & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) 
        & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])

    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

if __name__ == '__main__':
    code = '000001.XSHE'
    data = week_period_strategy(code, 'daily', '2024-01-01', '2024-03-01')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal', 'signal']])
    