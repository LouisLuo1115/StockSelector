import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ..data_crawler.data_crawler import crawl_price_by_date

def pr(x, population):
    return sum(population <= x) / sum(population.notnull())

def hitstock(date_1, date_2, top_n=20):
    # now = datetime.now().strftime('%Y%m%d')
    # last_week = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    print("Let's Predit Hit Stock!!!")
    data_1 = crawl_price_by_date(date_1)
    data_2 = crawl_price_by_date(date_2)
    data = data_1.merge(data_2, on='證券代號', how='inner')
    data = data[data['證券名稱_x'].str.len() <= 4]

    data['收盤價_x'] = pd.to_numeric(data['收盤價_x'], errors='coerce')
    data['收盤價_y'] = pd.to_numeric(data['收盤價_y'], errors='coerce')
    data['price'] = (data['收盤價_x'] - data['收盤價_y']) / data['收盤價_y']
    data['volume'] = (data['成交股數_x'] - data['成交股數_y']) / data['成交股數_y']

    data['price'] = data['price'].apply(pr, population=data['price'])
    data['volume'] = data['volume'].apply(pr, population=data['volume'])

    data['score'] = data['volume'] + data['price']
    top_n_list_code = data.nlargest(top_n, 'score')['證券代號'].tolist()
    top_n_list_name = data.nlargest(top_n, 'score')['證券名稱_x'].tolist()
    
    top_n_str = ''
    for code, name in zip(top_n_list_code, top_n_list_name):
        top_n_str = top_n_str + code + ':' + name + '\n'
    
    with open('./data/topn_stock_data/{}.txt'.format(date_2), 'w') as f:
        f.write(top_n_str)
    
    print(top_n_str)
    print('Job Done!!!')

if __name__ == "__main__":
    hitstock('20210810', '20210809')
