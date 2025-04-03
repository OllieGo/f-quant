from jqdatasdk import *
import datetime
import pandas as pd
import os

auth('username','password')

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)



'''获取股票估值指标'''
# df = get_fundamentals(query(valuation), date=None , statDate="2024")

# print(df)




'''获取股票财务指标'''
df = get_fundamentals(query(indicator), statDate="2024")
df = df[(df['eps'] > 0) & (df['roe'] > 10) & (df['inc_net_profit_year_on_year'] > 10)]
# 设置code作为df索引
df.index = df['code']
# print(df.head())


# df_slelct = pd.DataFrame()
# df_slelct['eps'] = df['eps']
# df_slelct['roe'] = df['roe']
# df_slelct['inc_net_profit_year_on_year'] = df['inc_net_profit_year_on_year']
# print(df_slelct)

'''获取股票估值指标'''
df_valuation = get_fundamentals(query(valuation), date=None , statDate="2024")
df_valuation.index = df_valuation['code']
# print(df_valuation.head())

df['pe_ratio'] = df_valuation['pe_ratio']
df = df[(df['pe_ratio'] < 30)]
print(df)