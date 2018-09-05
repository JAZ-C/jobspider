#coding: utf8

import requests

class IpProxy(object):

    def __init__(self):
        self.proxy_url = "http://192.168.78.131:8000/{}{}" #代理IP运行主机IP地址
        self.https_proxy = self.get_proxy("https")
        self.http_proxy = self.get_proxy()

    def get_proxy(self, type="http"):
        protocol = 0 if type == "http" else 1
        rv = requests.get(self.proxy_url.format("?types=0&count=1&protocol=", protocol)).json()
        proxy = ":".join(map(str, rv[0][0:2])) if rv else ""
        return proxy

    def delete_proxy(self, ip):
        # print(ip)
        requests.get(self.proxy_url.format("delete?ip=", ip))
