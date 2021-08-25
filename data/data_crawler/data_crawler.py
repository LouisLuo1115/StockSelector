import requests
from io import StringIO
import numpy as np
import pandas as pd

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

if __name__ == "__main__":
    df = crawl_price_by_date(20210805)
    print(df.head())
    df.to_csv('data.csv', index=False, encoding='utf_8_sig')