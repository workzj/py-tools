#coding=utf8
import itchat
import urllib, sys
import json

def format_result(s):
    message = u'大哥~~！！今天是' + s['result']['week'] + \
              ' ' + s['result']['weather']+'天，' + u'当前温度：' + s['result']['temp']+'，'\
              + u'最高温：'+ s['result']['temphigh']+'，'\
              + u'最底温：'+ s['result']['templow']+'，'\
              + u'湿度：'+ s['result']['humidity']+'，'\
              + u'风力：'+ s['result']['windpower']+'，'\
              + u'PM2.5：'+ s['result']['aqi']['ipm2_5']+ '，'\
              + u'空气质量：'+ s['result']['aqi']['quality'] +'。\n'\
              + u'求大哥赏口饭吃吧~！！！吐血跪谢~！！！'
    return message

def get_weather(city):
    host = 'http://jisutqybmf.market.alicloudapi.com'
    path = '/weather/query'
    method = 'GET'
    appcode = 'e5f90cd9ae684694a51d3c0f14889fa6'
    querys = 'city='+urllib.parse.quote(city)
    bodys = {}
    url = host + path + '?' + querys

    print(urllib.parse.unquote("%E5%AE%89%E9%A1%BA"))
    print(urllib.parse.quote("郑州"))

    request = urllib.request.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        print(content.decode('utf-8'))
        s = json.loads(content.decode('utf-8'))
        print(s['result']['aqi'])
        return format_result(s)

@itchat.msg_register('Text')
def text_reply(msg):
    if u'傻逼' in msg['Text'] or u'主人' in msg['Text']:
        return u'是你'
    elif u'天气' in msg['Text'] or u'获取' in msg['Text']:
        # itchat.send('@fil@main.py', msg['FromUserName'])
        return get_weather(u'郑州')
    elif u'获取图片' in msg['Text']:
        itchat.send('@img@applaud.gif', msg['FromUserName']) # there should be a picture
    else:
        return u'收到：' + msg['Text']

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({ 'Picture': u'图片', 'Recording': u'录音',
        'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
        u'已下载到本地') # download function is: msg['Text'](msg['FileName'])

@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias']

@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):
    if msg['isAt']:
        return u'@%s\u2005%s' % (msg['ActualNickName'],u'收到：' + msg['Text'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'项目主页：github.com/workzj/wechat_weather\n'
        + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
        + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])

itchat.auto_login(True, enableCmdQR=True)
itchat.run()

# get_weather(u'郑州')