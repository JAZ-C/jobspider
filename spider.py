#coding: utf8

import requests
import random
from bs4 import BeautifulSoup
from ipproxy import IpProxy
from retrying import retry
import re

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

class Spider:
    def __init__(self):
        self.session = requests.session()
        self.baseUrl = 'https://www6.pearsonvue.com'
        self.fullUrl = 'https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE'

    @property
    def headers(self):
        user_agent = random.choice(USER_AGENTS)
        return {
          "User-Agent": user_agent,
          "Host": "www6.pearsonvue.com",
          "Origin": "https://www6.pearsonvue.com"
        }

    @property
    def key(self):
        res = self.session.get(self.fullUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        key = soup.find(id="javax.faces.ViewState")["value"]
        return key

    @retry(stop_max_attempt_number=3)
    def login(self):
        data = {
            "inputUserName": "wq12345",
            "inputPassword": "ceshiMIMA123../",
            "submitButton": "Sign In",
            "SignInForm_SUBMIT": 1,
            "javax.faces.ViewState": self.key
        }
        headers = self.headers
        headers["Referer"] = "https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE"
        try:
            try_proxy = IpProxy().http_proxy
            try_proxys = IpProxy().https_proxy
            try_proxies = {
                "https": "https://{}".format(try_proxys),
                "http": "http://{}".format(try_proxy)
            }
            IpProxy().delete_proxy(try_proxy.split(":")[0])
            res = self.session.post(url=self.fullUrl, data=data, headers=headers, proxies=try_proxies, timeout=50)
            self.http_proxy = try_proxy
            self.proxies = try_proxies
            soup = BeautifulSoup(res.text, 'html.parser')
            url = soup.select('#examCatalogContainer a')[0]['href']
            self.fetch_dashboard(url)
        except Exception as e:
            print(e)

    def fetch_dashboard(self, url):
        res = self.session.get(self.baseUrl + url, headers=self.headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.select("#maincontent form")[0]
        key = form.find(id="javax.faces.ViewState")["value"]
        id = form["id"]
        action = form["action"]
        self.getProvideAnswers(id, key, url, action)

    def getProvideAnswers(self, id, key, url, action):
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
        form = soup.find(id='examRegistrationQuestionsForm')
        self.getSearchPage(form, url)

    def getSearchPage(self, form, url):
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
        form = soup.find(id="testCenterFormId")
        self.searchform = form
        self.searchurl = url

    def searchList(self, address):
        self.login()
        action = self.searchform['action']
        key = self.searchform.find(id="javax.faces.ViewState")["value"]
        data = {
          "geoCodeLatitude": 31.2303904,
          "geoCodeLongitude": 121.47370209999997,
          "geoCodeTwoCharCountryCode": "CN",
          "ambiguousSearchResult": "",
          "mapAvailable": True,
          "uiSearchSelected": True,
          "testCenterCode": "",
          "fullAddress": address,
          "testCenterSearch": "Search",
          "testCenterFormId_SUBMIT": 1,
          "javax.faces.ViewState": key
        }
        headers = self.headers
        headers['Referer'] = self.baseUrl + self.searchurl
        res = self.session.post(self.baseUrl + action, data=data, headers=headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        tc_name_list = [x.string.strip() for x in soup.select('.tc_name')] if  soup.select('.tc_name') else []
        tc_address = [re.match(r'<div class="tc_address">(.*)', str(x)).group(1).split('<br/>')  for x in soup.select('.tc_address')] if soup.select('.tc_address') else []
        tc_href_list = [x.a['href'].strip() for x in soup.select(".tc_info") ] if soup.select(".tc_info") else []
        tc_id = [x.a['id'].split("_")[1] for x in soup.select(".tc_info") ] if soup.select(".tc_info") else []
        tc_info = list(zip(tc_name_list, tc_address, tc_id, tc_href_list))
        return tc_info

    def get_tcinfo(self, id, url):
        try_proxy = IpProxy().http_proxy
        try_proxys = IpProxy().https_proxy
        try_proxies = {
            "https": "https://{}".format(try_proxys),
            "http": "http://{}".format(try_proxy)
        }
        data = {
            "testCenterId": id,
            "clientCode": "PEARSONLANGUAGE"
        }
        res = self.session.get(self.baseUrl + url, data=data, headers=self.headers, proxies=try_proxies)
        soup = BeautifulSoup(res.text, 'html.parser')
        tc_name = soup.find(class_="tc_name").text.strip()
        tc_address = soup.find(class_="tc_address").text.strip()
        tc_phone = soup.find(class_="tc_phone").text.strip()
        tc_dir = soup.find(class_="directions").text.strip()
        tc_all = [tc_address, tc_phone, tc_dir]
        tc_info = {tc_name: tc_all}
        return tc_info


# print(Spider().searchList('shanghai'))