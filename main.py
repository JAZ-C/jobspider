#coding: utf8

import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




def get_proxy():
  return requests.get("http://123.207.35.36:5010/get/").content.split(":")

def delete_proxy(proxy):
  requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))



class Spider:
  def __init__(self):
    self.session = requests.session()
    self.baseUrl = 'https://www6.pearsonvue.com'

  @property
  def headers(self):
    return {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

  """
  发起请求
  url: url,
  method: method [get, post],
  data: data,
  pageName: 请求页面保存的文件名
  """
  def makeRequest(self, url = '', method = 'post', data = {}, pageName = 'index.html'):
    # proxyHttps = requests.get('http://127.0.0.1:8111/proxy?count=1&anonymity=anonymous&protocol=https').json()[0]
    # proxyHttp = requests.get('http://127.0.0.1:8111/proxy?count=1&anonymity=anonymous&protocol=http').json()[0]
    proxyHttp = get_proxy()
    proxies = {
      "http": "http://{0}:{1}".format(proxyHttp[0], proxyHttp[1]),
      # "https": "https://{0}:{1}".format(proxyHttps[0], proxyHttps[1])
    }
    headers = self.headers
    # headers['X-Forwarded-For'] = proxy[0]
    # headers['X-Real-IP'] = proxy[0]
    print('proxies: ', proxies)
    if method == 'post':
      res = self.session.post(url, data, headers=headers, proxies=proxies)
    else:
      res = self.session.get(url, headers=headers, proxies=proxies)

    file = open('./pages/' + pageName, 'w')
    file.write(res.text.encode('utf-8',"ignore"))

    if 'You reached this page when trying to access' in res.text:
      print('error')
      exit(1)

    return BeautifulSoup(res.text, 'html.parser')

  """
  页面中提交表单需要发起一个状态
  id=javax.faces.ViewState
  """
  def getStateKey(self, soup):
    return soup.find(id="javax.faces.ViewState")["value"]

  def start(self):
    self.getLoginStateKey()

  """
  首页
  """
  def getLoginStateKey(self):
    soup = self.makeRequest(self.baseUrl + '/testtaker/signin/SignInPage/PEARSONLANGUAGE', 'get', pageName='index.html')
    key = self.getStateKey(soup)
    self.login(key)

  """
  登录
  """
  def login(self, key):
    data = {
      "inputUserName": "yuqing2132",
      "inputPassword": "youNI2132",
      "submitButton": "Sign In",
      "SignInForm_SUBMIT": 1,
      "javax.faces.ViewState": key
    }
    soup = self.makeRequest(url=self.baseUrl + '/testtaker/signin/SignInPage/PEARSONLANGUAGE', method='post', data=data, pageName="login.html")
    url = soup.select('#examCatalogContainer a')[0]['href']
    print(url)
    self.getExamCatalogInfo(key, url)

  def getExamCatalogInfo(self, key, url):
    data = {
        "javax.faces.ViewState": key
    }
    soup = self.makeRequest(url=self.baseUrl + url, method="get", pageName="examCatalogInfo.html")
    url = soup.select()






sp = Spider()

sp.start()