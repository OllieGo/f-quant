
from jqdatasdk import *
import time
import datetime
import os
import pandas as pd

auth('username','password')

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)

# 全局变量
data_root = '/pythonCoding/f-quant/data/'

"""
初始化股票数据库
return: 
"""
def init_db():
    # 1.获取所有股票代码
    stocks = get_stock_list()
    # 2.存储到scv中
    for code in stocks:
        start_date='2024-02-04'
        end_date='2025-02-10'
        df = get_single_price(code, 'daily', start_date, end_date)
        export_data(df, code, 'price')
        print(code)
        print(df.head()) 

"""
获取所有A股股票列表
XSHG-上海证券交易所
XSHE-深圳证券交易所
return: stocks_list
"""
def get_stock_list():
    stocks_list = list(get_all_securities(types=['stock']).index)
    return stocks_list

"""
获取单个股票行情数据
param: code
param: time_freq
param: start_date
param: end_date
return: 
"""
def get_single_price(code, time_freq, start_date=None, end_date=None):
    # 如果start_date=None，默认为从上市日期开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()

    # 获取行情数据
    data = get_price(code, start_date = start_date, end_date = end_date
                     , frequency = time_freq)
    return data

"""
导出股票行情数据
param: data
param: filename
param: type 股票数据类型:price、finance
param: mode a代表追加,none代表默认w写入
return: 
"""
def export_data(data, filename, type, mode=None):
    file_root = data_root + type + '/' + filename + '.csv'

    try:
        data.index.names = ['date']
        if mode == 'a':
            if os.path.exists(file_root):
                # 文件存在，则以追加模式写入，不添加列名
                data.to_csv(file_root, mode='a', header=False)
                
                # 读取并去重
                data = pd.read_csv(file_root, index_col='date') # 使用date作为索引读取数据
                data = data[~data.index.duplicated(keep='last')]  # 去除重复行，保留最后一条记录
                
                data.to_csv(file_root) # 重新写入
                print(f"Data successfully appended to {file_root}")
            else:
                # 文件不存在，则创建新文件并写入数据
                data.to_csv(file_root)
                print(f"Data successfully saved to new file {file_root}")
            
        else:
            data.to_csv(file_root)
            print(f"Data successfully saved to new file {file_root}")
    except Exception as e:
        print(f"Failed to save data to {file_root}: {e}")

"""
从csv读取数据
param: code
param: type
return: 
"""
# def get_csv_data(code, type):
#     file_root = data_root + type + '/' + code + '.csv'
#     return pd.read_csv(file_root)


"""
获取本地数据，且完成数据更新工作
param: code: str,股票代码
param: start_date: str,起始日期
param: end_date: str,起始日期
return: dataframe
"""
def get_csv_price(code, start_date, end_date):
    # 使用update直接更新
    update_daily_price(code)
    
    # 读取数据
    file_root = data_root + 'price/' + code + '.csv'
    data = pd.read_csv(file_root, index_col= 'date')
    # print(data)
    
    # 根据日期筛选股票数据
    return data[(data.index >= start_date) & (data.index <= end_date)]


"""
将数据转化为指定周期：开盘价（周期第一天）、收盘价（周期最后一天）、最高价（周期内）、最低价（周期内）
param: data
param: time_freq
return: 
"""
def transfer_price_freq(data, time_freq):
 
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()

    return df_trans

"""
获取单个股票财务指标
param: code
param: date
param: statDate
return: 
"""
def get_single_finance(code, date, statDate):
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statDate)
    return data


"""
获取单个股票估值指标
param: code
param: date
param: statDate
return: 
"""
def get_single_valuation(code, date, statDate):
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)
    return data

"""
涨跌幅 = （当期收盘价 - 前期收盘价）/ 前期收盘价）
param: data: dataframe,带有收盘价
return: dataframe,带有涨跌幅
"""
def caculate_change_pct(data):
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data

def update_daily_price(stock_code, type='price'):
    # 3.1是否存在文件：不存在-重新获取，存在->3.2
    file_root = data_root + type + '/' + stock_code + '.csv'
    if os.path.exists(file_root): # 如果存在对应文件
        # 3.2获取增量数据（code, start_date=对应股票csv中的最新日期，end_date=今天）
        startdate = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1]
        # enddate = datetime.datetime.today()
        enddate = '2025-02-15'
        df = get_single_price(stock_code, 'daily', startdate, enddate)
        # 3.3追加到已有文件中
        export_data(df, stock_code, 'price', 'a')

    else:
        # 重新获取股票行情数据
        df = get_single_price(stock_code)
        export_data(df, stock_code, 'price')
    
    print("股票已经更新成功：", stock_code)
    