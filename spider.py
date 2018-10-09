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
        # 初始化session
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
        try_proxy = IpProxy().http_proxy
        try_proxies = {
            # "https": "https://{}".format(try_proxys),
            "http": "http://{}".format(try_proxy)
        }
        res = self.session.get(self.fullUrl, timeout=50, headers=self.headers, proxies=try_proxies)
        soup = BeautifulSoup(res.text, 'html.parser')
        key = soup.select("#SignInForm input[name='javax.faces.ViewState']")[0]["value"]
        return key


    def login(self):
        """
        执行登录
        :return: 下一级页面登录url
        """
        data = {
            "inputUserName": "yuqing2132", # 用户名
            "inputPassword": "youNI2132", # 密码
            "submitButton": "Sign In",
            "SignInForm_SUBMIT": 1,
            "javax.faces.ViewState": self.key # 每一次请求必要带上一页面的key
        }
        headers = self.headers
        headers["Referer"] = "https://www6.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE"
        # 使用代理登录
        # try:
        try_proxy = IpProxy().http_proxy
        # try_proxys = IpProxy().https_proxy
        try_proxies = {
            # "https": "https://{}".format(try_proxys),
            "http": "http://{}".format(try_proxy)
        }
        IpProxy().delete_proxy(try_proxy.split(":")[0])
        res = self.session.post(url=self.fullUrl, data=data, headers=headers, proxies=try_proxies, timeout=50)
        self.http_proxy = try_proxy
        self.proxies = try_proxies
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.select('#examCatalogContainer a')[0]['href']
        self.conversationId = url.split('=')[-1]
        # self.fetch_dashboard(url)
        return url
        # except Exception as e:
        #     print(e)

    def fetch_dashboard(self, url):
        res = self.session.get(self.baseUrl + url, headers=self.headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.select("#maincontent form")[0]
        key = form.select("input[name='javax.faces.ViewState']")[0]["value"]
        id = form["id"]
        action = form["action"]
        return id, key, url, action

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
        return form, url

    def getSearchPage(self, form, url):
        action = form["action"]
        key = form.select("input[name='javax.faces.ViewState']")[0]["value"]
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
        return form

    def searchList(self, form, address):
        """
        查询具体地址列表
        :param form:    上一级页面表单
        :param address: 搜索地点 "e.g : beijing"
        :return:
        """
        if not form:
            return {}
        action = form['action']
        key = form.select("input[name='javax.faces.ViewState']")[0]["value"]
        locationInfo = self.getLocationInfo(address)
        data = {
          "geoCodeLatitude": locationInfo["location"]["lat"],
          "geoCodeLongitude": locationInfo["location"]["lng"],
          "geoCodeTwoCharCountryCode": locationInfo["code"],
          "ambiguousSearchResult": "",
          "mapAvailable": True,
          "uiSearchSelected": True,
          "testCenterCode": "",
          "fullAddress": address,
          "testCenterSearch": "Search",
          "selectedDistanceUnit": 0,
          "unitVal": "mi",
          "testCenterFormId_SUBMIT": 1,
          "javax.faces.ViewState": key
        }
        headers = self.headers
        res = self.session.post(self.baseUrl + action, data=data, headers=headers, proxies=self.proxies, timeout=50)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.find(id="testCenterFormId")
        datekey = form.select("input[name='javax.faces.ViewState']")[0]["value"]
        tc_name_list = [x.string.strip() for x in soup.select('.tc_name')] if  soup.select('.tc_name') else []
        tc_address = [re.match(r'<div class="tc_address">(.*)', str(x)).group(1).split('<br/>')  for x in soup.select('.tc_address')] if soup.select('.tc_address') else []
        tc_href_list = [x.a['href'].strip() for x in soup.select(".tc_info") ] if soup.select(".tc_info") else []
        tc_id = [x.a['id'].split("_")[1] for x in soup.select(".tc_info") ] if soup.select(".tc_info") else []
        # 考点列表
        tc_info = list(zip(tc_name_list, tc_address, tc_id, tc_href_list))
        return tc_info, datekey, locationInfo

    def getSearchDate(self,address, datekey, locationInfo, search_data):
        """
        查询具体地址可用日期
        address: 查询地点 "e.g :beijing"
        datekey: 上一级网页中的javax.faces.ViewState
        loacationInfo: 查询地点的地图信息
        search_data: 查询信息dict;
                     search_data['id'] 具体查询地址ID "e.g : 50488"
                     search_data['month'] 具体查询月份  "e.g : 9"
                     search_data['year'] 具体查询年份  "e.g : 2018"
        :return:
        """
        searchurl = "/testtaker/registration/SelectTestCenterProximity/PEARSONLANGUAGE/" + self.conversationId
        data = {
            "geoCodeLatitude": locationInfo["location"]["lat"],
            "geoCodeLongitude": locationInfo["location"]["lng"],
            "geoCodeTwoCharCountryCode": locationInfo["code"],
            "ambiguousSearchResult": "",
            "mapAvailable": True,
            "uiSearchSelected": True,
            "testCenterCode": "",
            "fullAddress": address,
            "selectedTestCenters": search_data.get('id'),
            "selectedDistanceUnit": 0,
            "unitVal": "mi",
            "continueTop": "Next",
            "testCenterFormId_SUBMIT": 1,
            "javax.faces.ViewState": datekey
        }

        headers = self.headers
        headers['Referer'] = "https://www6.pearsonvue.com/testtaker/registration/SelectTestCenterProximity/PEARSONLANGUAGE?conversationId=" + self.conversationId
        headers['Upgrade-Insecure-Requests'] = "1"
        res = self.session.post(self.baseUrl + searchurl, data=data, headers=headers, proxies=self.proxies, timeout=50)
        print(res)
        soup = BeautifulSoup(res.text, 'html.parser')
        jd_id = soup.select_one('script[id]').get('id')
        key = soup.select("input[name='javax.faces.ViewState']")[0]["value"]

        if not search_data.get('datetime'):
            date_data = {
                "AJAXREQUEST": "_viewRoot",
                "calendarForm:calendarMonth": "Month",
                "calendarForm:calendarDay": "Day",
                "calendarForm:apptdates": "Select one...",
                "selectedAppointmentId": "",
                "calendarForm": "calendarForm",
                "autoScroll": "",
                "javax.faces.ViewState": key,
                "month": search_data.get('month'),
                "year": search_data.get('year'),
                "AJAX:EVENTS_COUNT": 1
            }
            date_data[jd_id] = jd_id
            next_url = "/testtaker/registration/CalendarAppointmentSearchPage/PEARSONLANGUAGE"
            headers['Referer'] = 'https://www6.pearsonvue.com/testtaker/registration/CalendarAppointmentSearchPage/PEARSONLANGUAGE'
            res = self.session.post(self.baseUrl + next_url, data=date_data, headers=headers, proxies=self.proxies, timeout=50)
            file = open('111.html', 'w')
            file.write(res.text)
            new_soup = BeautifulSoup(res.text, 'html.parser')
            date_list = re.findall(r'availableDates\\":\[\\"(.*?)}', new_soup.select_one('span[id="_ajax:data"]').text)[0].\
                replace('\\\"','').replace('\\x5D','').split(',')
            # date_list = [x.get('value') for x in new_soup.select('option')][2:-1] #被遗弃的方法，有点小缺陷
            return date_list
        else:
            return key, soup

    def getSearchDateTime(self, key, soup, search_data):
        search_url = "/testtaker/registration/CalendarAppointmentSearchPage/PEARSONLANGUAGE/" + str(search_data.get('id'))
        j_id_list = soup.select('script[id]')
        j_id = ""
        for j in j_id_list:
            j_id = re.findall(r"ajaxSingle':'(.*?)'}", j.text)[0] if re.findall(r"ajaxSingle':'(.*?)'}", j.text) else j_id
        data = {
            "AJAXREQUEST": "_viewRoot",
            "calendarForm:calendarMonth": "Month",
            "calendarForm:calendarDay": "Day",
            "calendarForm:apptdates": "Select one...",
            "selectedAppointmentId": "",
            "calendarForm": "calendarForm",
            "autoScroll": "",
            "javax.faces.ViewState": key,
            "selectedDate": search_data.get('datetime'),
            "ajaxSingle": j_id,
            "AJAX:EVENTS_COUNT": 1
        }
        data[j_id] = j_id
        headers = self.headers
        headers['Referer'] = 'https://www6.pearsonvue.com/testtaker/registration/CalendarAppointmentSearchPage/PEARSONLANGUAGE'
        res = self.session.post(self.baseUrl + search_url, data=data, headers=headers, proxies=self.proxies, timeout=50)
        file = open('./test.html', 'w')
        file.write(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        time_info = re.findall(r'startTimeFormatted\\": \\"(.*?)\\"}', soup.select_one('span[id="_ajax:data"]').text)
        return time_info

    def doSearchData(self, address, search_data=None):
        fetch_url = self.login()
        id, key, url ,action = self.fetch_dashboard(fetch_url)
        form, url = self.getProvideAnswers(id, key, url, action)
        list_form = self.getSearchPage(form, url)
        rv_info, datekey, locationInfo = self.searchList(list_form, address)
        if not search_data:
            return rv_info
        elif not search_data.get('datetime'):
            rv_info = self.getSearchDate(address, datekey, locationInfo, search_data)
            return rv_info
        else:
            datetime_key, soup = self.getSearchDate(address, datekey, locationInfo, search_data)
            rv_info = self.getSearchDateTime(datetime_key, soup, search_data)
            return rv_info

    def get_tcinfo(self, id, url):
        try_proxy = IpProxy().http_proxy
        # try_proxys = IpProxy().https_proxy
        try_proxies = {
            # "https": "https://{}".format(try_proxys),
            "http": "http://{}".format(try_proxy)
        }
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

    def getLocationInfo(self, address):
        """
        获取城市详情
        """
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


if __name__ == "__main__":
    # print(Spider().doSearchData('beijing'))
    print(Spider().doSearchData('beijing', {'month': 9, 'year': 2018, 'id': 50488}))
    # print(Spider().doSearchData('beijing', {'month': 9, 'year': 2018, 'id': 50488, 'datetime': '10/16/2018'}))
