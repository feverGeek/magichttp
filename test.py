# coding: utf-8
import io
import mimetypes
import http.client

raw = """
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

 

鑺傜洰娓呭崟.txt
------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7
Content-Disposition: form-data; name="Filedata"; filename="鑺傜洰娓呭崟.txt"
Content-Type: application/octet-stream

 

锘�2009-11-06
05:30-05:59 1 鍔ㄧ敾涓栫晫
06:00-06:29 1 浣撹偛鏂伴椈
06:30-06:59 1 浜轰笌鑷劧
07:00-07:30 1 鏂伴椈鑱旀挱
------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7
Content-Disposition: form-data; name="Upload"

 

Submit Query
------------Ef1KM7GI3Ef1ei4Ij5ae0KM7cH2KM7--
"""

raw = raw.lstrip().encode()
raw = io.BytesIO(raw)
requestline = raw.readline()
print(requestline)
#l = raw.readline()

headers = http.client.parse_headers(raw)
content_type = headers.get('Content-Type', '')
print(content_type)