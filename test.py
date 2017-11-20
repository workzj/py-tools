__author__ = 'zhujiang'
# -*- coding: <utf-8> -*-
import urllib
import urllib.request
import urllib.parse

import urllib.request, urllib.parse, urllib.error
import socket

def requesturi(uri,msg):

    req = urllib.request.Request(uri+msg)
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode("utf-8")
    print(content)

def posturi():
    url = "http://10.100.207.56:7003/signClient"
    # details = urllib.parse.urlencode({'IDToken1': 'USERNAME', 'IDToken2': 'PASSWORD'})
    postdata = urllib.parse.urlencode({'email': 'yicui49@gmail.com', 'password': 'fashlets123', 'Submit': ''})
    url = urllib.request.Request('http://10.100.207.56:7003/signClient',postdata)
    url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")
    postdata = postdata.encode('utf-8')
    res = urllib.request.urlopen(url, postdata)
    print(res.status, res.reason)



def test_post():

    try:
        details = urllib.parse.urlencode({ 'IDToken1': 'USERNAME', 'IDToken2': 'PASSWORD' })
        details = details.encode('UTF-8')
        url = urllib.request.Request('http://10.100.207.56:7003/signClient', details)
        url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

        responseData = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
        responseFail = False
        print(responseData)

    except urllib.error.HTTPError as e:
        responseData = e.read().decode('utf8')
        print(responseData)
        responseFail = False

    except urllib.error.URLError:
        responseFail = True
        print('1')

    except socket.error:
        responseFail = True
        print('2')

    except socket.timeout:
        responseFail = True
        print('3')

    except UnicodeEncodeError:
        print("[x]  Encoding Error")
        responseFail = True

    # print(responseData)

if __name__ == '__main__':
    # msg = 'productid-'
    # for i in range(100):
    #     requesturi('http://localhost:8080/debt/auto_buy.do?message=',msg+str(i))
    test_post()

