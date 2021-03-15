import numpy as np
from pandas import DataFrame, Series
import pandas as pd
from datetime import datetime

def sort_date():
    df = pd.read_csv('E:\\datesort\\result.csv', encoding='utf8')
    df = DataFrame(df)
    df['DATE'] = pd.to_datetime(df['date'])
    df = df[['DATE','positive','negative']]
    df['DATE'] = [datetime.strftime(x, '%Y-%m-%d') for x in df['DATE']]
    df = df.pivot_table(index='DATE',values=[u'positive', u'negative'], aggfunc='sum')
    print(df)
    df.to_csv('result_sort.csv')
if __name__ == '__main__':
    sort_date()

