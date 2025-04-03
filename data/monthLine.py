
from jqdatasdk import *
import time
import pandas as pd

auth('username','password')

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)

# XSHG-上海证券交易所；XSHE-深圳证券交易所 000001.XSHE-平安银行 002555.XSHE-三七互娱
# df = get_price('002555.XSHE', count = 2, end_date='2024-12-29', frequency='daily', fields=['open', 'close']) # 获取获得000001.XSHG在2015年01月31日前2个交易日的数据

# df = get_price('002555.XSHE', count = 10, end_date='2024-12-29', frequency='1m') #1分钟数据
# df = get_price('002555.XSHE', count = 100, end_date='2024-12-29', frequency='daily')
# print(len(df))
# print(df)

# 获取A股所有股票数据
# stocks = get_all_securities(types=['stock'], date=None)
# print(stocks)

# df = get_price(['000001.XSHE', '002555.XSHE'], count = 10, end_date='2024-12-29', frequency='daily')
# print(df)


# stocks = get_price(['000001.XSHE', '002555.XSHE'], count = 10, end_date='2024-12-29', frequency='daily')
# print(df)


# 获取所有股票行情数据
# stocks = list(get_all_securities(types=['stock']).index)
# print(stocks)

# for stock_code in stocks:
#     print("正在获取股票行情数据，股票代码：", stock_code)
#     df = get_price(stock_code, count = 10, end_date='2024-12-29', frequency='daily')
#     print(df)
#     time.sleep(3)


# resample函数

# 获取日K
stock_code = '002555.XSHE'
df = get_price(stock_code, start_date='2023-01-01', end_date='2023-12-31', frequency='daily')
df['month'] = df.index.month
print(df)


# 获取月K
df_month = pd.DataFrame()
df_month['open'] = df['open'].resample('M').first()
df_month['close'] = df['close'].resample('M').last()
df_month['high'] = df['high'].resample('M').max()
df_month['low'] = df['low'].resample('M').min()

print(df_month)
