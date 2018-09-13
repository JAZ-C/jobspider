#coding: utf8

import requests
import random
from bs4 import BeautifulSoup
from ipproxy import IpProxy
# from retrying import retry
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
        self.hostName = 'wsr.pearsonvue.com'
        self.baseUrl = 'https://' + self.hostName
        self.userName = 'yuqing2132'
        self.password = 'youNI2132'

        self.proxies = None
        self.getProxy()
        self.user_agent = random.choice(USER_AGENTS)
    
    def getProxy(self, https=False):
        proxy = IpProxy()
        try:
            http_proxy = proxy.get_proxy()
            proxy.delete_proxy(http_proxy.split(':')[0])
            proxies = {
                "http": "http://{}".format(http_proxy)
            }
            if https:
                https_proxy = proxy.get_proxy('https')
                proxy.delete_proxy(https_proxy.split(':')[0])
                proxies["https"] = "https://{}".format(https_proxy)
            self.proxies = proxies
            print(self.proxies)
        except Exception as e:
            raise Exception('代理获取失败')

    def getHeaders(self, Referer=None):
        headers = {
          "User-Agent": self.user_agent,
          "Host": self.hostName,
          "Origin": self.baseUrl,
        }
        if Referer is not None:
            headers["Referer"] = Referer
        return headers

    def getPageKey(self, soup):
        return soup.find(id="javax.faces.ViewState")["value"]

    def getKey(self, url):
        soup = self.makeRequests(url=url, method='get', page="key.html")
        return self.getPageKey(soup)

    def makeRequests(self, url, data={}, headers=None, proxies=None, method="post", timeout=50, page=None):
        res = None
        if method == 'post':
            res = self.session.post(
                url=url,
                data=data,
                headers=headers if headers is not None else self.getHeaders(),
                proxies=proxies if proxies is not None else self.proxies,
                timeout=timeout
            )
        else:
            res = self.session.get(
                url=url,
                data=data,
                headers=headers if headers is not None else self.getHeaders(),
                proxies=proxies if proxies is not None else self.proxies,
                timeout=timeout
            )
        if res is not None:
            if page is not None:
                file = open('./pages/' + page, 'w')
                file.write(res.text)
            return BeautifulSoup(res.text, 'html.parser')
    
    """
    根据获取城市详情
    """
    # @retry(stop_max_attempt_number=3)
    def getLocationInfo(self, address):
        # googleMapUrl = "http://maps.googleapis.cn/maps/api/geocode/json?address=" + address # 需要翻墙
        # https://maps.googleapis.com/maps/api/geocode/json?address=shanghai+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyDSCL2P-emde6kzlSMLTr2YWs009yGKyU4
        # googleMapUrl = "https://ditu.google.cn/maps/api/geocode/json?language=zh-CN?&address=" + address + "+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyDSCL2P-emde6kzlSMLTr2YWs009yGKyU4"  # 不需要翻墙
        googleMapUrl = "https://ditu.google.cn/maps/api/geocode/json?language=zh-CN?&address=" + address + "&key=AIzaSyDSCL2P-emde6kzlSMLTr2YWs009yGKyU4"
        results = requests.get(googleMapUrl, timeout=10).json()["results"][0]
        result = {}
        for area in results["address_components"]:
            if 'country' in area["types"]:
                result["code"] = area["short_name"]
                break
        
        result["location"] = results["geometry"]["location"]
        return result

    def login(self, retry=True):
        url = self.baseUrl + '/testtaker/signin/SignInPage/PEARSONLANGUAGE'
        data = {
            "inputUserName": self.userName,
            "inputPassword": self.password,
            "submitButton": "Sign In",
            "SignInForm_SUBMIT": 1,
            "javax.faces.ViewState": self.getKey(url)
        }
        soup = self.makeRequests(url=url, data=data, headers=self.getHeaders(url), page="login.html")
        links = soup.select('#examCatalogContainer a')
        if links is None or len(links) == 0:
            IpProxy().delete_proxy(self.proxies['http'].split('//')[1].split(':')[0])
            if 'https' in self.proxies:
                IpProxy().delete_proxy(self.proxies['https'].split('//')[1].split(':')[0])
            print('ip error')
            if retry:
                self.getProxy()
                self.login(retry=False)
        self.searchUrl = self.baseUrl + soup.select('#examCatalogContainer a')[0]['href']
        self.fetch_dashboard()

    def fetch_dashboard(self):
        soup = self.makeRequests(url=self.searchUrl, page="dashboard.html")
        form = soup.select("#maincontent form")[0]
        self.getProvideAnswers(form)

    def getProvideAnswers(self, form):
        id = form['id']
        action = form['action']
        data = {
          "nextButton": "Schedule this Exam",
          id + ":_link_hidden_": "",
          id + ":_idcl": "",
          id + "_SUBMIT": "1",
          "javax.faces.ViewState": self.getPageKey(form)
        }
        soup = self.makeRequests(url=self.baseUrl + action, data=data, headers=self.getHeaders(self.searchUrl), page="getProvideAnswers.html")
        form = soup.find(id='examRegistrationQuestionsForm')
        self.getSearchPage(form)

    def getSearchPage(self, form):
        action = form["action"]
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
          "javax.faces.ViewState": self.getPageKey(form)
        }
 
        soup = self.makeRequests(url=self.baseUrl + action, data=data, headers=self.getHeaders(self.searchUrl), page="getSearchPage.html")
        form = soup.find(id="testCenterFormId")
        self.searchForm = form

    def searchList(self, address):
        action = self.searchForm['action']
        self.locationInfo = self.getLocationInfo(address)
        data = {
          "geoCodeLatitude": self.locationInfo["location"]["lat"],
          "geoCodeLongitude": self.locationInfo["location"]["lng"],
          "geoCodeTwoCharCountryCode": self.locationInfo["code"],
          "ambiguousSearchResult": "",
          "mapAvailable": True,
          "uiSearchSelected": True,
          "testCenterCode": "",
          "fullAddress": address,
          "testCenterSearch": "Search",
          "testCenterFormId_SUBMIT": 1,
          "javax.faces.ViewState": self.getPageKey(self.searchForm)
        }
        soup = self.makeRequests(url=self.baseUrl + action, data=data, headers=self.getHeaders(self.searchUrl), page="searchList.html")
        self.searchForm = soup.find(id="testCenterFormId")
        tc_name_list = [x.string.strip() for x in soup.select('.tc_name')] if  soup.select('.tc_name') else []
        tc_address = [re.match(r'<div class="tc_address">(.*)', str(x)).group(1).split('<br/>')  for x in soup.select('.tc_address')] if soup.select('.tc_address') else []
        tc_href_list = [x.a['href'].strip() for x in soup.select(".tc_info") ] if soup.select(".tc_info") else []
        tc_id = [x.a['id'].split("_")[1] for x in soup.select(".tc_info") ] if soup.select(".tc_info") else []
        tc_info = list(zip(tc_name_list, tc_address, tc_id, tc_href_list))
        print(tc_info)

    def getSearchDatePage(self, testCenterId):
        searchurl = self.baseUrl + "/testtaker/registration/SelectTestCenterProximity/PEARSONLANGUAGE"
        data = {
            "geoCodeLatitude": self.locationInfo["location"]["lat"],
            "geoCodeLongitude": self.locationInfo["location"]["lng"],
            "geoCodeTwoCharCountryCode": self.locationInfo["code"],
            "ambiguousSearchResult": "",
            "mapAvailable": True,
            "uiSearchSelected": True,
            "testCenterCode": "",
            "fullAddress": "ShangHai",
            "selectedTestCenters": str(testCenterId),
            "selectedDistanceUnit": "0",
            "unitVal": "mi",
            "continueBottom": "Next",
            "testCenterFormId_SUBMIT": 1,
            "javax.faces.ViewState": self.getPageKey(self.searchForm)
        }
        # def has_class_but_no_id(tag):
        # return tag.has_attr('class') and not tag.has_attr('id')
        def getFilteredTags(tag):
          if not tag.has_attr('id'):
            return False
          return tag.name == 'script' and tag['id'].startswith('calendarForm:j_id')
        soup = self.makeRequests(searchurl, data=data, headers=self.getHeaders(searchurl), page="searchData.html")
        self.searchForm = soup.find(id="calendarForm")
        scripts = soup.find_all(getFilteredTags)
        dateKey = None
        timeKey = None
        for script in scripts:
          id = script["id"]
          content = script.string
          if "getAvailableDaysAjax" in script.string:
            dateKey = script["id"]
          if "getAppointmentTimesForDayAjax" in script.string:
            timeKey = script["id"]
        
        return dateKey, timeKey
          
    def getAvailableDays(self, dateKey):
      url = self.baseUrl + '/testtaker/registration/CalendarAppointmentSearchPage/PEARSONLANGUAGE'
      data = {
        "AJAXREQUEST": "_viewRoot",
        "calendarForm:calendarMonth": "Month",
        "calendarForm:calendarDay": "Day",
        "calendarForm:apptdates": "Select one...",
        "selectedAppointmentId": "",
        "calendarForm": "calendarForm",
        "autoScroll": "",
        "javax.faces.ViewState": self.getPageKey(self.searchForm),
        dateKey: dateKey,
        "month": 10,
        "year": 2018,
        "AJAX:EVENTS_COUNT": 1,
      }
      soup = self.makeRequests(url=url, data=data, page="getAvailableDays.html")

    def get_tcinfo(self, id, url):
        data = {
            "testCenterId": id,
            "clientCode": "PEARSONLANGUAGE"
        }
        res = self.session.get(self.baseUrl + url, data=data, headers=self.headers, proxies=try_proxies)
        file = open('pages/test.html', 'w')
        file.write(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        tc_name = soup.find(class_="tc_name").text.strip()
        tc_address = soup.find(class_="tc_address").text.strip()
        tc_phone = soup.find(class_="tc_phone").text.strip()
        tc_dir = soup.find(class_="directions").text.strip()
        tc_all = [tc_name, tc_phone, tc_dir]
        tc_info = {"tc_info": tc_all}
        return tc_info

if __name__ == "__main__":
    sp = Spider()
    sp.login()
    print('login success')
    sp.searchList('shanghai')
    print('get searchlist success')
    dateKey, timeKey = sp.getSearchDatePage(50489)
    sp.getAvailableDays(dateKey)

