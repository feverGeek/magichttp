import requests
from requests.structures import CaseInsensitiveDict
import io
import http.client
import urllib.parse
from functools import wraps


"""
>>> import magichttp
>>> http_text = '''
POST /index.php/api/v2/user/contacts HTTP/1.1
Accept: application/json
user-agent: TAS-AN00(Android/7.1.2) (uni.UNIEB8DEE7) UniApp/0.28.0 900x1600
token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LnpoYW5nY2hhby5uYW1lIiwiYXVkIjoiaHR0cHM6XC9cL3d3dy56aGFuZ2NoYW8ubmFtZSIsImlhdCI6MTYxNTc5Nzk5NSwibmJmIjoxNjE1Nzk3OTk1LCJleHAiOjE2MTY0MDI3OTUsImRhdGEiOnsibWVtYmVyX2lkIjoxMDQ5MjZ9fQ.eZCF_ZDTYEipGjzbeVyIbA9FWyhH_C5ZUVH6wASa3nw
Content-Type: application/json; charset=utf-8
Content-Length: 10
Host: jiekou.ayao888.com
Connection: close
Accept-Encoding: gzip, deflate

{"res":[]}
'''

>>> obj = magichttp.MagicHttp(url,raw=http_text)
>>> obj.headers()
{
    "method": "POST",
    "accept": "application/json",
    "user-agent": "TAS-AN00(Android/7.1.2) (uni.UNIEB8DEE7) UniApp/0.28.0 900x1600",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LnpoYW5nY2hhby5uYW1lIiwiYXVkIjoiaHR0cHM6XC9cL3d3dy56aGFuZ2NoYW8ubmFtZSIsImlhdCI6MTYxNTc5Nzk5NSwibmJmIjoxNjE1Nzk3OTk1LCJleHAiOjE2MTY0MDI3OTUsImRhdGEiOnsibWVtYmVyX2lkIjoxMDQ5MjZ9fQ.eZCF_ZDTYEipGjzbeVyIbA9FWyhH_C5ZUVH6wASa3nw",
    "content-type": "application/json; charset=utf-8",
    "content-length": 10,
    "host": "jiekou.ayao888.com",
    "connection": "close",
    "accept-encoding": "gzip, deflate"
}

>>> obj.body()
{"res":[]}

>>> resp = obj.request()
>>> resp
<Response [200]>
>>> resp.text
>>> resp.content


>>> obj = magichttp.MagicHttp(url)
>>> resp = obj.request()
>>> resp
<Response [200]>


>>> obj = magichttp.MagicHttp(url)
>>> resp = obj.request('POST', data='key1=value1&key2=value2')
>>> resp
<Response [200]>


"""

def default_user_agent():
    return 'Mozilla/5.0 (X11; FreeBSD amd64; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'


def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({
        'user-agent': default_user_agent(),
        'accept-encoding': ', '.join(('gzip', 'deflate')),
        'accept': '*/*',
        'connection': 'keep-alive',
    })


def lower_keys(dict):
    new_dict = {}
    for k, v in dict.items():
        new_dict.update({k.lower(): v})
    return new_dict


def http_strip(http_text):
    temp = ''
    http_text = http_text.lstrip()
    list = http_text.split('\n')
    for i in list:
        temp += i.lstrip() + '\n'
    return temp


class MagicHttp:
    def __init__(self, url, **kwargs):
        """
        :param url: URL 
        :param raw: http request package
        """

        def get_urlinfo(url=None):
            if url:
                parse_result = urllib.parse.urlparse(url)
                scheme = parse_result.scheme.lower()
                if scheme != 'http' and scheme != 'https':
                    raise Exception("scheme must be http or https")
                host = parse_result.netloc
                if path := parse_result.path:
                    raise Exception("invalid host: %s" % url)
                return host, url
            else:
                raise Exception("url cannot be empty")

        def _http():
            pass

        def parse_raw(url, raw=None):
            host, url = get_urlinfo(url)

            if raw:
                raw = http_strip(raw).encode()
                raw = io.BytesIO(raw)
                requestline = raw.readline().decode()
                words = requestline.split()
                if len(words) == 3:
                    self.__method, self.__path, _ = words
                elif len(words) == 2:
                    self.__method, self.__path = words
                else:
                    raise Exception('http raw parse error')

                self.__headers = CaseInsensitiveDict(
                    http.client.parse_headers(raw))

                raw_body = b''
                content_type = self.__headers.get('content-type', '')
                if content_type.startswith('multipart/form-data'):
                    while True:
                        line = raw.readline()
                        if line == b'':
                            raw_body = raw_body[:-2]
                            break
                        if line[:2] == b'--':
                            if raw_body != b'' and raw_body[-2:] != b'\r\n':
                                raw_body = raw_body[:-1] + b'\r\n'
                            raw_body += line.rstrip() + b'\r\n'
                        elif line[:8].lower() == b'content-':
                            raw_body += line.rstrip() + b'\r\n'
                            line = raw.readline()
                            if line[:8].lower() == b'content-':
                                raw_body += line.rstrip() + b'\r\n'
                                raw.readline()
                            raw_body += b'\r\n'
                        else:
                            raw_body += line
                else:
                    while True:
                        line = raw.readline()
                        if line == b'':
                            raw_body = raw_body[:-2] # 去掉末尾的\r\n
                            break
                        raw_body += line.rstrip() + b'\r\n'

                raw.close()

                if self.__headers.get('host') and self.__headers['host'] != host:
                    raise Exception("raw data's host(%s) not equal url(%s)" %(self.__headers['host'], host))
                self.__headers['content-length'] = str(len(raw_body))
                self.__raw_body = raw_body
                self.__url = url + self.__path
            else:
                self.__headers = default_headers()
                self.__headers['host'] = host
                self.__method = 'GET'
                self.__raw_body = None
                self.__path = '/'
                self.__url = url + self.__path

        self.raw = kwargs.get('raw')
        parse_raw(url, self.raw)

    def path(self):
        return self.__path

    def headers(self):
        """
        return http request headers
        :rtype: str
        """
        prefix = "{\n"
        pattern = "\t\"{key}\": \"{value}\",\n"
        suffix = "}\n"
        string = "".join(pattern.format(key='method', value=self.__method))
        for k, v in self.__headers.items():
            string += pattern.format(key=k.lower(), value=v)
        string = string[:-2] + '\n'
        return prefix + string + suffix

    def body(self):
        """
        return http request body
        """
        return self.__raw_body

    # def request(self, method=None, params=None, data=None, json=None, **kwargs):
    def request(self, method=None, **kwargs):
        """
        :param method: (optional) request method 
        :param params: (optional) Dictionary
        :param headers: (optional) Dictionary of HTTP Headers
        :param data: (optional) Dictionary
        :param json (optional) json data

        :param **kwargs: Optional arguments

        :return: :class:`Response <Response> object`
        :rtype: requests.Response
        """

        if method:
            self.__method = method.upper()

        if self.__method.upper() == 'GET':
            params = kwargs.pop('params') if kwargs.get('params') else None
            headers = kwargs.pop('headers') if kwargs.get('headers') else self.__headers 
            return requests.get(self.__url, params=params, headers=headers, **kwargs)

        elif self.__method.upper() == 'OPTIONS':
            return requests.options(self.__url, **kwargs)

        elif self.__method.upper() == 'HEAD':
            return requests.head(self.__url, **kwargs)

        elif self.__method.upper() == 'POST':
            data = kwargs.pop('data') if kwargs.get('data') else self.__raw_body
            print(type(data))
            json = kwargs.pop('json') if kwargs.get('json') else None
            headers = kwargs.pop('headers') if kwargs.get('headers') else self.__headers 
            # TODO: 将self.__raw_body 转成字典 
            return requests.post(self.__url, data=data, json=json, headers=headers)

        elif self.__method.upper() == 'PUT':
            data = kwargs.pop('data') if kwargs.get('data') else None
            return requests.put(self.__url, data=data, **kwargs)

        elif self.__method.upper() == 'PATCH':
            data = kwargs.pop('data') if kwargs.get('data') else None
            return requests.patch(self.__url, data=data, **kwargs)

        elif self.__method.upper() == 'DELETE':
            return requests.delete(self.__url, **kwargs)