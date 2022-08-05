import io
from urllib.parse import urlparse
from black import Encoding
from regex import F
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
# import concurrent.futures
import multiprocessing
from multiprocessing import Process,freeze_support
from multiprocessing import Pool
#import concurrent.futures
import os

import warnings
warnings.filterwarnings('ignore')


def CPU_bound(i,j,q):
    df=pd.DataFrame(columns=['url','title','subtitle','image','claps','responses','reading time','publication','author_name','author_pic','date'])
    for t in range(i,j+1):
        # print(f'Processing Data File {t}',end='\r',flush=True)
        print(t)
        with open('{}.txt'.format(t),'r',encoding='utf8') as file:
                page_contents=file.read()
        doc=BeautifulSoup(page_contents,'html.parser')
        divs=doc.find_all('div',{'class':'postArticle postArticle--short js-postArticle js-trackPostPresentation js-trackPostScrolls'})
        for div in divs:
            lis=[]
            if div.find('a',{'class':"link link--darken"}) is None:
                lis.append('')
            else:
                lis.append(div.find('a',{'class':"link link--darken"})['href'])


            #title
            if div.find('h3',{'class':'graf--title'}) is None:
                lis.append('')
            else:
                import unicodedata
                lis.append(unicodedata.normalize("NFKD",div.find('h3',{'class':'graf--title'}).text))

            #subtitle
            if div.find('h4',{'class':'graf--subtitle'}) is None:
                lis.append('')
            else:
                lis.append(div.find('h4',{'class':'graf--subtitle'}).text)

            #image
            if div.find('img',{'class':"graf-image"}) is None:
                lis.append('')
            else:
                lis.append(div.find('img',{'class':"graf-image"})['src']) 

            #claps
            if div.find('span',{'class':'u-relative u-background js-actionMultirecommendCount u-marginLeft5'}) is None:
                lis.append('')
            else:
                lis.append(div.find('span',{'class':'u-relative u-background js-actionMultirecommendCount u-marginLeft5'}).text)

            #responses
            if div.find('div',{'class':"buttonSet u-floatRight"}) is None:
                lis.append('')

            else:
                lis.append(div.find('div',{'class':"buttonSet u-floatRight"}).text.split(' ')[0])

            #reading_time
            if div.find('span',{'class':"readingTime"}) is None:
                lis.append('')
            else:
                lis.append(div.find('span',{'class':"readingTime"})['title'].split(' min')[0])

            #publication
            if div.find('a',{'class':'ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal'}) is None:
                lis.append('')
            else:
                lis.append(div.find('a',{'class':'ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal'}).text)

            # author_name
              
            if div.find('a',{'class':"ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken"}) is None:
                lis.append('')
            else:
                lis.append(div.find('a',{'class':"ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken"}).text)

            # author_pic
            if div.find('img',{'class':"avatar-image u-size36x36 u-xs-size32x32"}) is None:
                lis.append('')
            else:
                lis.append(div.find('img',{'class':"avatar-image u-size36x36 u-xs-size32x32"})['src'])

            #date
            if div.find('time') is None:
                lis.append('')
            else:
                lis.append(div.find('time')['datetime'][:10])          
    
            dl=pd.DataFrame([lis],columns=['url','title','subtitle','image','claps','responses','reading time','publication','author_name','author_pic','date'])
            df=df.append(dl)

    df.reset_index(drop=True,inplace=True)
    # df.to_excel("Check_data.xlsx",index=True,sheet_name='Scraped Data')
    q.put(df)
    #return df

# CPU_bound(0,18)
     
      

if __name__=="__main__":
 
 q=multiprocessing.Manager().Queue()
#  os.makedirs('Data')
#  import numpy as np
 freeze_support()


 p1=multiprocessing.Process(target=CPU_bound,args=(0,638,q))
 p2=multiprocessing.Process(target=CPU_bound,args=(639,1277,q))
 p3=multiprocessing.Process(target=CPU_bound,args=(1278,1916,q))
 p4=multiprocessing.Process(target=CPU_bound,args=(1917,2554,q))

 p1.start()
 p2.start()
 p3.start()
 p4.start()

 p1.join()
 p2.join()
 p3.join()
 p4.join()


 df=pd.DataFrame(columns=['url','title','subtitle','image','claps','responses','reading time','publication','author_name','author_pic','date'])
 while q.empty() is False:
        df=df.append(q.get())
    
 df.reset_index(drop=True,inplace=True)
#  df.to_excel("Output_new_2.xlsx",index=True,sheet_name='Scraped Data')
 df.to_csv("dataframe_output",index=True)




