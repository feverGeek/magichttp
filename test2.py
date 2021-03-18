# coding:utf-8
import json
from magichttp import MagicHttp
from magichttp import lower_keys
from requests.structures import CaseInsensitiveDict


def _main():
    raw = '''
POST /index.php/api/v2/user/contacts HTTP/1.1
Accept: application/json
user-agent: TAS-AN00(Android/7.1.2) (uni.UNIEB8DEE7) UniApp/0.28.0 900x1600
token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LnpoYW5nY2hhby5uYW1lIiwiYXVkIjoiaHR0cHM6XC9cL3d3dy56aGFuZ2NoYW8ubmFtZSIsImlhdCI6MTYxNTc5Nzk5NSwibmJmIjoxNjE1Nzk3OTk1LCJleHAiOjE2MTY0MDI3OTUsImRhdGEiOnsibWVtYmVyX2lkIjoxMDQ5MjZ9fQ.eZCF_ZDTYEipGjzbeVyIbA9FWyhH_C5ZUVH6wASa3nw
Content-Type: application/json; charset=utf-8
Content-Length: 10
Host: jiekou.ayao888.com
Connection: close
Accept-Encoding: gzip, deflate

c=3&d=4'''

    raw2 = """
POST /load/servlet/upload.do HTTP/1.1
accept:text/*
content-type:multipart/form-data; boundary=----------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7
user-agent:Shockwave Flash
host:192.168.1.237:8080
content-length:555
connection:Keep-Alive
cache-control:no-cache
cookie:theworld_client_delete=theworld_client_delete

 

------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7
Content-Disposition: form-data; name="Filename"

 

文件.txt
------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7
Content-Disposition: form-data; name="Filedata"; filename="文件.txt"
Content-Type: application/octet-stream

 

文件2009-11-06
05:30-05:59 1 测试数据
06:00-06:29 1 测试数据
06:30-06:59 1 测试数据
07:00-07:30 1 测试数据
------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7
Content-Disposition: form-data; name="Upload"

 

Submit Query
------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7--
"""

    raw3 = """
GET /down.php/../../../../../../../../../etc/passwd HTTP/1.1
User-Agent: Mozilla/5.0 (X11; FreeBSD amd64; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

"""

    # r = MagicHttp(url="http://127.0.0.1:8090",raw=raw3)
    # # print(dir(r))
    # print(r.path())
    # print(r.headers())
    # print(r.body())
    # print()
    # r.request()

    r = MagicHttp(url="http://127.0.0.1:8090", raw=raw)
    # print(dir(r))
    print(r.path())
    print(r.headers())
    print(r.body())
    print()
    jsondata = json.dumps({"a":2, "b":3}) 
    r.request(params="a=1&b=2", json=jsondata)

    # r = MagicHttp(url="http://jiekou.ayao888.com/index.php/api/v2/user/contacts")
    # print(r.headers())
    # print(r.body())
    # print()
    # r.request()

    # r = MagicHttp(url="http://jiekou.ayao888.com/index.php/api/v2/user/contacts")
    # r.request('GET')

    # r = MagicHttp(url="http://jiekou.ayao888.com/index.php/api/v2/user/contacts")
    # r.request('GET', params="a=1&b=2")
    
    # r = MagicHttp(url="http://192.168.1.237:8080/load/servlet/upload.do", raw=raw2)
    # print(r.headers())
    # print(r.body())

if __name__ == '__main__':
    _main()