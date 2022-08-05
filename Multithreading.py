import requests
import time
import pandas as pd
import concurrent.futures 
# import threading
import io
from black import Encoding
from regex import F

from bs4 import BeautifulSoup

import random




start='2021-01-01'
end='2021-12-31'
dates=pd.date_range(start, end)

urls=[
    'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}', # 64
    'https://uxdesign.cc/archive/{0}/{1:02d}/{2:02d}', # 15
    'https://medium.com/swlh/archive/{0}/{1:02d}/{2:02d}', # 74
    'https://writingcooperative.com/{0}/{1:02d}/{2:02d}', # 6
    'https://medium.com/datadriveninvestor/archive/{0}/{1:02d}/{2:02d}', # 41
    'https://medium.com/better-humans/archive/{0}/{1:02d}/{2:02d}', # 2
    'https://medium.com/better-marketing/archive/{0}/{1:02d}/{2:02d}'
]



t1 = time.perf_counter()
i=0

def download_data(date):
 for url in urls:
    data = requests.get(url.format(date.year,date.month,date.day)).text
    print(date)
    global i
    data_name=f'{i}.txt'
    i=i+1
    print(data_name)
    with open(data_name,'w',encoding='utf8') as data_file:
        data_file.write(data)
        print(' was downloaded...')


with concurrent.futures.ThreadPoolExecutor() as executor:
  executor.map(download_data, dates)



t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')
