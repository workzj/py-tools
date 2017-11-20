__author__ = 'zhujiang'
# -*- coding: <utf-8> -*-
import urllib.request
import urllib.parse
import http.client

import json
import time
import datetime
import re
import os
import random
import json
import pymysql
import datetime
import csv


def testDEV():
    day=input("请输入日期：")
    print(day)
    req = urllib.request.Request('http://dev.360.cn/mobileappstat/appdownload?soft_id=3010649&callback=sssss&type=hour&day='+day)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')
    req.add_header('Host', 'dev.360.cn')
    req.add_header('Cookie', '__guid=137882464.3605513999081097000.1443506427031.3918; Q=u%3D%25OO%25O0%25O7%25Q1%25O9%25O7%26n%3D%26le%3Drzuiozq5nJAunGVjZGDyAQNkAwZhL29g%26m%3DZGt1WGWOWGWOWGWOWGWOWGWOZmtk%26qid%3D1327750986%26im%3D1_t00df551a583a87f4e9%26src%3Dpcw_open_app%26t%3D1; T=s%3Dac59850807c111980c31d20e188e9e3d%26t%3D1443509304%26lm%3D%26lf%3D1%26sk%3D743647ee066faff8f92d6aa3d74239be%26mt%3D1443509304%26rc%3D%26v%3D2.0%26a%3D1; test_cookie_enable=null; count=5')
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode("utf-8")
    print(content)
    a1 = re.compile(r"sssss\((.*?)\)")
    d = a1.findall(content)
    #print(d)
    s = json.loads(d[0])
    print(s["data"])

    EXCEL_DATA = []
    for data in s["data"]:
        EXCEL_DATA.append([time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(data["date"]/1000)),data["value"]])


    with open(day+'.csv', 'w',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(['时间','次数'])
        for item in EXCEL_DATA:
            spamwriter.writerow(item)



testDEV()





