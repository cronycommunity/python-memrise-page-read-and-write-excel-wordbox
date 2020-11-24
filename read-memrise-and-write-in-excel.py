from selenium import webdriver
import numpy as np
import pandas as pd
import time
import tqdm
import re
import os, shutil
browser = webdriver.Chrome()
browser.maximize_window() #maximum resolution
# browser.set_window_size(1366,768)#optional resolution
browser.get('https://www.memrise.com/course/1338049/almanca-b21-kelimeler-ve-gramatik/')

xx=(''.join(list(''.join(browser.find_element_by_xpath('//*[@id="content"]/div/div/div[1] ').text))))# toplamda kac seviye oldugunu bulmak icin
data = re.split("\n", xx)                                                                            #
new_data = [data[0]+"\n"]+["\n" + i for i in data[1:-1]] + ["\n"+data[-1]]                           #

levelist1=[i[8:]  if i.startswith('\nNiveau') else i[6:] if i.startswith('\nTeil') else None for i in new_data ]
levelist1=[i for i in levelist1 if i is not None]

for i in tqdm.tqdm(levelist1):
    browser.get('https://www.memrise.com/course/1338049/almanca-b21-kelimeler-ve-gramatik/{}/'.format(i))  
    all_spans = browser.find_elements_by_xpath("//*[contains(.,'text')]")                            # sayfadaki bütün textleri cekiyoruz
    # all_spans = browser.find_element_by_css_selector(".col_a col text")
    list1=[]
    for ii in all_spans:
        list1.append(ii.text)
    list1 = [x.strip().split("\n") for x in list1]
    list1=list1[0]
    list1=list1[list1.index('Bereit zum lernen       Bereit zum Wiederholen')+1:list1.index('Über uns')]        # ortadaki kismi bizim tablomuz
    df=pd.DataFrame({'almanca':list1[0::2],'turkce':list1[1::2]})
    if not os.path.exists('MemriseTable.csv'):
        df.to_csv('MemriseTable.csv')
    else:
        df.to_csv('MemriseTableB1_1.csv',mode='a',header=False)

df=pd.read_csv('MemriseTable.csv',index_col=0).reset_index().drop('index',axis=1)
df = df.join(df['turkce'].str.split(',', expand=True).add_prefix('turkce')).drop('turkce',axis=1)
df.to_excel('MemriseTable.xlsx')
print(df.to_string())
