from jqdatasdk import *
import time
import pandas as pd
import os

auth('username','password')

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)



'''获取股票财务指标'''
df = get_fundamentals(query(indicator), statDate="2023")
print(df)
# df.to_csv('/data/finance/finance2023.csv')



# 修改为相对路径或绝对路径，确保目录存在
output_dir = os.path.join(os.getcwd(), 'data', 'finance')  # 使用当前工作目录下的data/finance作为输出目录
os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，则创建之

output_path = os.path.join(output_dir, 'finance2023.csv')
df.to_csv(output_path, index=False)
print(f"Data successfully saved to {output_path}")