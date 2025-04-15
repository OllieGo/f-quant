
from jqdatasdk import *
import time
import os
import pandas as pd

auth('16605815273','Mydream1994')

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)

# 全局变量
data_root = '/pythonCoding/f-quant/data/'

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
def get_single_price(code, time_freq, start_date, end_date):
    # 如果start_date=None，默认为从上市日期开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    # 获取行情数据
    data = get_price(code, start_date = start_date, end_date = end_date
                     , frequency = time_freq)
    return data

"""
导出股票行情数据
param: data
param: filename
param: type 股票数据类型:price、finance
return: 
"""
def export_data(data, filename, type):
    file_root = data_root + type + '/' + filename + '.csv'

    try:
        data.index.names = ['date']
        
        if os.path.exists(file_root):
            # 文件存在，则以追加模式写入，不添加列名
            data.to_csv(file_root, mode='a', header=False)
            print(f"Data successfully appended to {file_root}")
        else:
            # 文件不存在，则创建新文件并写入数据
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
def get_csv_data(code, type):
    file_root = data_root + type + '/' + code + '.csv'
    return pd.read_csv(file_root)

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