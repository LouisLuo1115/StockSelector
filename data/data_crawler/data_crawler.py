import time
import random
import requests
from urllib.request import urlopen, Request
import json
from io import StringIO
from datetime import date, timedelta
import datetime
from dateutil import rrule
import numpy as np
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def crawl_price_by_date(date):
    date = str(date).replace('-', '')
    try:
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date + '&type=ALL')
        df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        df = df.apply(lambda s: pd.to_numeric(s.astype(str).str.replace(",", "").replace("+", "1").replace("-", "-1").replace("X", "0"), errors='ignore'))
        df = df[['證券代號', '證券名稱', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌(+/-)', '漲跌價差', '最後揭示買價', '最後揭示買量', '最後揭示賣價', '最後揭示賣量', '本益比']]
        print('Success crawl {} stock data!'.format(date))
        return df
    except:
        print('Fail to crawl {} stock data'.format(date))

def crawl_indiv_stock_price_by_date(stock_number, date):
    url = (
        "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+
        date.strftime('%Y%m%d')+
        "&stockNo="+
        str(stock_number)
    )
    time.sleep(random.uniform(1.1, 5.5))
    # headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
    # data_1 = Request(url, headers=headers)
    # data = json.loads(urlopen(data_1).read())

    data = json.loads(urlopen(url).read())
    print(date.strftime('%Y%m%d'))
    return pd.DataFrame(data['data'], columns=data['fields'])

def crawl_indiv_stock_price_history(stock_number, start_month):
    b_month = date(*[int(x) for x in start_month.split('-')])
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    e_month = date(*[int(x) for x in now.split('-')])
    result = pd.DataFrame()
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=b_month, until=e_month):
        result = pd.concat([result, crawl_indiv_stock_price_by_date(stock_number, dt)], ignore_index=True)
        time.sleep(random.uniform(0.1, 2.1))
    
    return result

if __name__ == "__main__":
    df = crawl_price_by_date(20210805)
    print(df.head())
    df.to_csv('data.csv', index=False, encoding='utf_8_sig')