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
      'http': "http://" + ":".join(map(str, self.http_proxy)),
      # 'http': "http://" + ".join(map(str, self.http_proxy)),
    }

  @property
  def headers(self):
    return {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
      "Host": "www6.pearsonvue.com",
      "Origin": "https://www6.pearsonvue.com"
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
    header = self.headers
    header["Referer"] = "https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE"
    res = self.session.post(url=self.fullUrl, data=data, headers=header, proxies=self.proxies, timeout=50)
    file = open('./pages/login.html', 'w')
    file.write(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    url = soup.select('#examCatalogContainer a')[0]['href']
    return url

  def fetchDashboard(self, url):
    file = open('./pages/fetchDashboard.html', 'w')
    # res = file.read()
    res = self.session.get(self.baseUrl + url, headers=self.headers, proxies=self.proxies, timeout=50)
    soup = BeautifulSoup(res.text, 'html.parser')
    file.write(res.text)
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
    file.write(res.text)
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
    form = soup.find(id="testCenterFormId")
    self.searchList(form, url)

  def searchList(self, form, url):
    file = open('./pages/result.html', 'w')
    action = form['action']
    key = form.find(id="javax.faces.ViewState")["value"]
    data = {
      "geoCodeLatitude": 31.2303904,
      "geoCodeLongitude": 121.47370209999997,
      "geoCodeTwoCharCountryCode": "CN",
      "ambiguousSearchResult": "",
      "mapAvailable": True,
      "uiSearchSelected": True,
      "testCenterCode": "",
      "fullAddress": "shanghai",
      "testCenterSearch": "Search",
      "testCenterFormId_SUBMIT": 1,
      "javax.faces.ViewState": key
    }
    headers = self.headers
    headers['Referer'] = self.baseUrl + url
    res = self.session.post(self.baseUrl + action, data=data, headers=headers, proxies=self.proxies, timeout=50)
    soup = BeautifulSoup(res.text, 'html.parser')
    file.write(res.text)
    print(res)


def start(sp):
  loginKey = sp.getLoginKey()
  print(loginKey)
  dashboardUrl = sp.login(loginKey)
  print(dashboardUrl)
  sp.fetchDashboard(dashboardUrl)


# @retry
def main():
  sp = Spider()
  # try:
  start(sp)
    # sp.delete_proxy(sp.https_proxy[0])
  # except Exception as e:
  #   print(e)
  #   print(sp.http_proxy[0], sp.https_proxy[0])
  #   sp.delete_proxy(sp.http_proxy[0])
  #   raise ValueError
    # sp.delete_proxy(sp.https_proxy[0])


main()
