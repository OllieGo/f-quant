
import sys
sys.path.append("D:/pythonCoding/f-quant")

import data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt

# 容器：存放夏普
sharpes = []

# 获取3只股票数据:比亚迪、宁德时代、隆基
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
for code in codes:
    data = st.get_single_price(code, 'daily', '2024-01-29', '2025-02-04')
    print(data.head())

    # 计算每只股票夏普率
    daily_sharpe, annual_sharpe = stb.calculate_sharpe(data)
    sharpes.append([code, annual_sharpe]) # 存放[[c1,s1],[c2,s2]..]
    print(sharpes)

# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')
print(sharpes)

# 绘制bar图
sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=30)
plt.show()
