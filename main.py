#coding: utf8

import requests
from bs4 import BeautifulSoup
from ipproxy import IpProxy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_proxy():
  return requests.get("http://192.168.111.129:8000/?types=0&count=1&protocol=1&country=国内").json()

def delete_proxy(proxy):
  requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

class Spider:
    def __init__(self):
        self.session = requests.session()
        self.baseUrl = 'https://www6.pearsonvue.com'
        self.fullUrl = 'https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE'
        self.http_proxy = IpProxy().http_proxy
        self.https_proxy = IpProxy().https_proxy
        self.proxies = {
            'http': "http://{}".format(self.http_proxy)
        }

    @property
    def headers(self):
        return {
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
          "Host": "www6.pearsonvue.com",
          "Origin": "https://www6.pearsonvue.com"
        }

    @property
    def key(self):
        res = self.session.get(self.fullUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        key = soup.find(id="javax.faces.ViewState")["value"]
        return key

    def login(self, key):
        data = {
            "inputUserName": "yuqing2132",
            "inputPassword": "youNI2132",
            "submitButton": "Sign In",
            "SignInForm_SUBMIT": 1,
            "javax.faces.ViewState": key
        }
        headers = self.headers
        headers["Referer"] = "https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE"

        res = self.session.post(url=self.fullUrl, data=data, headers=headers, proxies=self.proxies, timeout=50)
        file = open('./pages/login.html', 'w')
        file.write(res.text.encode('utf-8', "ignore"))
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.select('#examCatalogContainer a')[0]['href']
        self.fetch_dashboard(url)

    def fetch_dashboard(self, url):
        file = open('./pages/fetchDashboard.html', 'w')
        res = self.session.get(self.baseUrl + url, headers=self.headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        file.write(res.text.encode('utf-8', "ignore"))
        form = soup.select("#maincontent form")[0]
        key = form.find(id="javax.faces.ViewState")["value"]
        id = form["id"]
        action = form["action"]
        self.getProvideAnswers(id, key, url, action)

    def getProvideAnswers(self, id, key, url, action):
        file = open('./pages/ProvideAnswers.html', 'w')
        data = {
          "nextButton": "Schedule this Exam",
          id + ":_link_hidden_": "",
          id + ":_idcl": "",
          id + "_SUBMIT": "1",
          "javax.faces.ViewState": key
        }
        headers = self.headers
        headers['Referer'] = self.baseUrl + url
        res = self.session.post(self.baseUrl + action, data=data, headers=headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        file.write(res.text.encode('utf-8', "ignore"))
        form = soup.find(id='examRegistrationQuestionsForm')
        self.getSearchPage(form, url)

    def getSearchPage(self, form, url):
        file = open('./pages/searchPage.html', 'w')
        action = form["action"]
        key = form.find(id="javax.faces.ViewState")["value"]
        data = {
          "parentQuestionsIds_component1_SELECT_ONE_RADIOBUTTON_3422": "",
          "component1_SELECT_ONE_RADIOBUTTON_3422": 1,
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_2945": "",
          "component1_SELECT_ONE_LISTBOX_2945": "AFR",
          "parentQuestionsIds_component1_TEXT_3394": "",
          "component1_TEXT_3394": 34234,
          "component1_SELECT_ONE_CHECKBOX_2970": True,
          "component1_SELECT_ONE_CHECKBOX_3395": True,
          "component1_SELECT_ONE_CHECKBOX_3016": True,
          "parentQuestionsIds_component1_SELECT_MANY_CHECKBOX_5145": "",
          "component1_SELECT_MANY_CHECKBOX_5145": "Study DIBP / INZ 01",
          "component1_SELECT_MANY_CHECKBOX_5145": "Study DIBP / INZ 02",
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_3858": "",
          "component1_SELECT_ONE_LISTBOX_3858": "Internet search",
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_4560": "",
          "component1_SELECT_ONE_LISTBOX_4560": "My own country",
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_3860": "",
          "component1_SELECT_ONE_LISTBOX_3860": "Study",
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_3862": "",
          "component1_SELECT_ONE_LISTBOX_3862": "Not Studying",
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_4567": "",
          "component1_SELECT_ONE_LISTBOX_4567": "Not Studying",
          "parentQuestionsIds_component1_SELECT_ONE_LISTBOX_5155": "",
          "component1_SELECT_ONE_LISTBOX_5155": "No",
          "component1_component_handler": form.find(id="component1_component_handler")["value"],
          "nextButton": "Next",
          "examRegistrationQuestionsForm:_link_hidden_": "",
          "examRegistrationQuestionsForm:_idcl": "",
          "examRegistrationQuestionsForm_SUBMIT": 1,
          "javax.faces.ViewState": key
        }
        headers = self.headers
        headers['Referer'] = self.baseUrl + url
        res = self.session.post(self.baseUrl + action, data=data, headers=headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        file.write(res.text)
        print(res)


#   """
#   发起请求
#   url: url,
#   method: method [get, post],
#   data: data,
#   pageName: 请求页面保存的文件名
#   """
#   def makeRequest(self, url = '', method = 'post', data = {}, pageName = 'index.html'):
#     # proxyHttps = requests.get('http://127.0.0.1:8111/proxy?count=1&anonymity=anonymous&protocol=https').json()[0]
#     # proxyHttp = requests.get('http://127.0.0.1:8111/proxy?count=1&anonymity=anonymous&protocol=http').json()[0]
#     proxyHttps = get_proxy()
#     proxies = {
#       "https": "https://{0}:{1}".format(proxyHttps[0][0], proxyHttps[0][1]),
#       # "https": "https://{0}:{1}".format(proxyHttps[0], proxyHttps[1])
#     }
#     headers = self.headers
#     # headers['X-Forwarded-For'] = proxy[0]
#     # headers['X-Real-IP'] = proxy[0]
#     print('proxies: ', proxies)
#     if method == 'post':
#       res = self.session.post(url, data, headers=headers, proxies=proxies)
#     else:
#       res = self.session.get(url, headers=headers, proxies=proxies)
#
#     file = open('./pages/' + pageName, 'w')
#     file.write(res.text.encode('utf-8',"ignore"))
#
#     if 'You reached this page when trying to access' in res.text:
#       print('error')
#       exit(1)
#
#     return BeautifulSoup(res.text, 'html.parser')
#
#   """
#   页面中提交表单需要发起一个状态
#   id=javax.faces.ViewState
#   """
#   def getStateKey(self, soup):
#     return soup.find(id="javax.faces.ViewState")["value"]
#
#   def start(self):
#     self.getLoginStateKey()
#
#   """
#   首页
#   """
#   def getLoginStateKey(self):
#     soup = self.makeRequest(self.baseUrl + '/testtaker/signin/SignInPage/PEARSONLANGUAGE', 'get', pageName='index.html')
#     key = self.getStateKey(soup)
#     self.login(key)
#
#   """
#   登录
#   """
#   def login(self, key):
#     data = {
#       "inputUserName": "yuqing2132",
#       "inputPassword": "youNI2132",
#       "submitButton": "Sign In",
#       "SignInForm_SUBMIT": 1,
#       "javax.faces.ViewState": key
#     }
#     soup = self.makeRequest(url=self.baseUrl + '/testtaker/signin/SignInPage/PEARSONLANGUAGE', method='post', data=data, pageName="login.html")
#     url = soup.select('#examCatalogContainer a')[0]['href']
#     print(url)
#     self.getExamCatalogInfo(key, url)
#
#   def getExamCatalogInfo(self, key, url):
#     data = {
#         "javax.faces.ViewState": key
#     }
#     soup = self.makeRequest(url=self.baseUrl + url, method="get", pageName="examCatalogInfo.html")
#     url = soup.select()
#
#
#
def start(sp):
  loginKey = sp.key
  print(loginKey)
  sp.login(loginKey)

sp = Spider()
start(sp)
