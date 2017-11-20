__author__ = 'zhujiang'
# -*- coding: <utf-8> -*-
import urllib.request
import urllib.parse
import http.client

import json
import time
import re
import os
import random
import json
import pymysql
import datetime

path = os.path.dirname(__file__)

"""
    mobile  中国移动
    unicom  中国联通
    telcom  中国电信

    tmall   天猫
    wechat  微信
    jd      京东
"""

DATA_RESULT = []
IPS = {"移动":"mobile","联通":"unicom","电信":"telcom"}
JDIPS = {"1":"mobile","0":"unicom","2":"telcom"}
AREACODE={1:"北京",2:"上海"}

class SearchResult:
    "搜索结果的数据定义"
    def __init__(self,face=10,price=0.0,channel='tmall',isp='mobile',area='beijing'):
        self.face=face
        self.price=price
        self.channel=channel
        self.isp=isp
        self.area=area

def tmall(tel,isp):
    global DATA_RESULT
    req = urllib.request.Request('http://hf.m.tmall.com/getInitInfoForFlow.htm?_ksTS=1436253689105_54&callback=jsonp55&phone='+tel)
    req.add_header('Referer', 'http://wt.tmall.com/wtwidget/flow.htm')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')
    req.add_header('Host', 'hf.m.tmall.com')
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode("utf-8")
    #print(content)
    a1 = re.compile(r"\((.*?)\)")
    #a1 = re.compile("\((.*)\)")
    d = a1.findall(content)
    #print('************************************************')
    #print(d)
    s = json.loads(d[0])
    #print(s["globalItemList"])
    for item in s["globalItemList"]:
        ret = SearchResult(item['face'],float(item['price']),'tamll',isp)
        DATA_RESULT.append(ret)


def wechat():
    global DATA_RESULT
    req = urllib.request.Request('http://chong.qq.com/mobile/wx_traffic.shtml')
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode("utf-8")
    a1 = re.compile("jdata\.trafficPriceRules=\[([\s\S]*?)\];")
    #print(content)
    d = a1.findall(content)

    #print('***********************************')
    '''
    print(d[0])

    json_string=d[0].replace('area','\"area\"').replace('isp','\"isp\"').replace('prix','\"prix\"').replace('scope','\"scope\"')
    json_string=json_string.replace('effective','\"effective\"')
    json_string=json_string.replace('tips','\"tips\"')

    print(json_string)
    '''
    ####json_string = '['+json_string+']'
    json_string = '['+d[0]+']'
    s = json.loads(json_string)

    for item in s:
        global DATA_RESULT
        #print(item['area'])
        #if item['area']=="北京" :
            #print('北京 。。。。 ')
            #print(IPS[item['isp']])
        for val in item['prix']:
            face = int(int(val) / 100)
            if face>1000:
                face = int(face/1000)*1000
            ret = SearchResult(str(face),float(item['prix'][val][0]),'wechat',IPS[item['isp']],item['area'])
            DATA_RESULT.append(ret)
                #print(item['prix'][val][0],face)


def jd(area,isp):
    global DATA_RESULT
    req = urllib.request.Request('http://liuliang.jd.com/ajax/search_searchSku.action?areaCode=%d&mutCode=%s' % (area,isp))
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode("GBK")
    #print(content)
    s = json.loads(content)
    for item in s['country']:
        face = int(item['faceAmount'])
        if face>1000:
            face = int(face/1000)*1000

        ret = SearchResult(str(face),float(item['salePrice']),'jd',JDIPS[isp],AREACODE[area])
        DATA_RESULT.append(ret)
        """
        print(item['faceAmount'])
        print(item['salePrice'])
        print(JDIPS[isp])"""

def insertDB():
    SQL = "insert into `box_monitordataflow` (`face`,`price`,`isp`,`area`,`channel`,`grabtime`) values "#(<face>,<price>,<isp>,<area>,<channel>)
    global DATA_RESULT
    for item in DATA_RESULT:
        SQL = SQL + "('%s',%f,'%s','%s','%s','%s')" % (item.face,item.price,item.isp,item.area,item.channel,datetime.datetime.now())+','

    SQL=SQL[:-1]+';'
    print(SQL)

    try:
        print('begin connect')
        conn=pymysql.connect(host='zhongyicai.mysql.rds.aliyuncs.com',user='zhongyicai',passwd='dogfee20141115begin',db='dogfeetest',port=3306,charset='utf8')
        cur=conn.cursor()#获取一个游标
        print('execute sql ...')
        cur.execute(SQL)
        conn.commit()
        print('execute end ..')
        cur.close()#关闭游标
        conn.close()#释放数据库资源
    except  Exception :print("发生异常")

wechat()

#北京
jd(1,'0')#联通
jd(1,'1')#移动
jd(1,'2')#电信

#上海
jd(2,'0')#联通
jd(2,'1')#移动
jd(2,'2')#电信


tmall('15810609295','mobile')
tmall('15313719458','telcom')
tmall('18612185092','unicom')

tmall('18502156367','unicom')   #上海联通

for item in DATA_RESULT:
    print(item.face,item.price,item.channel,item.isp)

insertDB()


