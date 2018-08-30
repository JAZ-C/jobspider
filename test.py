import requests
from bs4 import BeautifulSoup
import sys
from retrying import retry

class Spider:

  def __init__(self):
    self.session = requests.session()
    self.baseUrl = 'https://www6.pearsonvue.com'
    self.fullUrl = 'https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE'
    self.https_proxy = self.get_proxy_https()
    self.http_proxy = self.get_proxy_http()
    self.proxies = {
      'http': "http://" + ":".join(map(str, self.https_proxy)),
      # 'http': "http://" + ".join(map(str, self.http_proxy)),
    }

  @property
  def headers(self):
    return {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
      "Referer": "https://www6.pearsonvue.com/testtaker/registration/Dashboard/PEARSONLANGUAGE/876050"
    }

  def get_proxy_https(self):
    return requests.get("http://127.0.0.1:8000/?types=0&count=1").json()[0][0:2]

  def get_proxy_http(self):
    return requests.get("http://127.0.0.1:8000/?types=0&count=1&protocol=0").json()[0][0:2]

  def delete_proxy(self, proxy):
    requests.get("http://127.0.0.1:8000/delete?ip={}".format(proxy))

  def getLoginKey(self):
    print(self.proxies)
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
    res = self.session.post(url=self.fullUrl, data=data, headers=self.headers, proxies=self.proxies, timeout=20)
    file = open('./pages/login.html', 'w')
    file.write(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    url = soup.select('#examCatalogContainer a')[0]['href']
    return url

  def fetchDashboard(self, url):
    file = open('./pages/fetchDashboard.html', 'w')
    # res = file.read()
    res = self.session.get(self.baseUrl + url, headers=self.headers, proxies=self.proxies, timeout=20)
    file.write(res.text)
    print(res)


def start(sp):
  loginKey = sp.getLoginKey()
  print(loginKey)
  dashboardUrl = sp.login(loginKey)
  print(dashboardUrl)
  sp.fetchDashboard(dashboardUrl)


@retry
def main():
  sp = Spider()
  try:
    start(sp)
    sp.delete_proxy(sp.https_proxy[0])
  except Exception as e:
    print(e)
    print(sp.http_proxy[0], sp.https_proxy[0])
    sp.delete_proxy(sp.http_proxy[0])
    raise ValueError
    # sp.delete_proxy(sp.https_proxy[0])


main()
