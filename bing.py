__author__ = 'zhujiang'
# -*- coding: <utf-8> -*-

import urllib.request, urllib.parse
from urllib.request import urlopen, urlretrieve
import json
import os

def download(url,name):
    target_dir = 'G:\\bing\\'

    urlretrieve(url, target_dir + name+'.jpg')



if __name__ == '__main__':
    req = urllib.request.Request('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&mkt=en-US')
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode("utf-8")
    s = json.loads(content)
    print(s["images"])
    for x in s["images"]:
        print('=========================')
        url = 'http://www.bing.com'+x['url']
        print(url)
        download(url,x['startdate'])
