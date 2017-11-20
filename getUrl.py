__author__ = 'zhujiang'

import urllib.request
from bs4 import BeautifulSoup
import json
import time
res = {}

def getBaiduTOPWord(dic,url='http://top.baidu.com/buzz?b=341&fr=topbuzz_b1',decode='GBK'):
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode(decode)
    soup = BeautifulSoup(html)
    result_list = soup.find_all("td",{"class":"keyword"})

    for child in result_list:
        print(child.find_next_sibling("td",{"class":"last"}))
        count = int(child.find_next_sibling("td",{"class":"last"}).span.string)
        print(count)
        dic[str(child.a.string.encode(encoding="utf-8").decode('utf-8'))] = count

    dic = sorted(dic.items(), key=lambda d:d[1], reverse=True)

    for key in dic:
        print(key)

def getHaosouTOPWord(dic,url='http://top.haosou.com/index.php?m=Hotnews&a=detail&type=week_hot',decode='utf-8'):
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode(decode)
    print(html)
    soup = BeautifulSoup(html)

    result_list = soup.find_all("td",class_="rankitem__info")

    for child in result_list:
         dic[child.div.a.string] = int(child.find_next_sibling("td",class_="rankitem__action").string)
    dic = sorted(dic.items(), key=lambda d:d[1], reverse=True)

    for key in dic:
        print(key)

while True:
    time.sleep(1)
    getBaiduTOPWord(res)
    with open('hotword.info', mode='w', encoding='utf-8') as f:
        json.dump(res,f,indent=2,ensure_ascii=False)

