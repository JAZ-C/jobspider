const puppeteer = require('puppeteer');
const proxyChain = require('proxy-chain');
const got = require('got');

const ip = require('./ip');

let requesting = false;

const sleep = async time => {
 return new Promise(resolve => {
   setTimeout(resolve, time)
 });
}

const detectRequesting = async () => {
  return new Promise(async(resolve, reject) => {
    let times = 0;
    // while (requesting) {
    //   await sleep(10);
    // }
    while (requesting && times < 100) {
      await sleep(117);
      console.log(times);
      times++;
    }
    resolve();
  });
}

class PearsonSpider {

  /**
   *等待元素加载完成
   *
   * @param {string} selector 元素选择器
   * @memberof PearsonSpider
   */
  async waitForSelector(selector){
    await this.page.waitForSelector(selector, {
      timeout: 50 * 1000
    });
  }

  /**
   *点击事件
   *
   * @param {string} selector 选择器, 需要点击的元素
   * @memberof PearsonSpider
   */
  async click(selector){
    await this.waitForSelector(selector);
    await this.page.click(selector);
  }

  /**
   *输入方法, 使用页面输入框
   *
   * @param {string} selector 选择器
   * @param {string} value 输入文本
   * @memberof PearsonSpider
   */
  async type(selector, value){
    await this.waitForSelector(selector);
    await this.page.type(selector, value);
  }

  /**
   *选择方法, 适用页面下拉框
   *
   * @param {*} selector
   * @param {*} value
   * @memberof PearsonSpider
   */
  async select(selector, value){
    await this.waitForSelector(selector);
    await this.page.select(selector, value);
  }

  /**
   *初始化资源, 开启爬虫任务
   *
   * @memberof PearsonSpider
   */
  async init() {
    const oldProxyUrl = await ip();
    // const newProxyUrl = await proxyChain.anonymizeProxy(oldProxyUrl);
    const browser = await puppeteer.launch({
      args: [`--proxy-server=${oldProxyUrl}`],
      defaultViewport: {
        width: 1000,
        height: 0
      },
      headless: false
    });

    const page = await browser.newPage();
    // 订阅事件 网络状态改变
    page.on('requestfailed', async () => {
      requesting = false;
      // console.log('network finished');
    });
    page.on('requestfinished', async () => {
      requesting = false;
      // console.log('network finished');
    });
    page.on('request', req => {
      requesting = true;
      // console.log('network started');
    });

    this.page = page;
  }

  /**
   * 开始爬取页面
   *
   * @param {*} page puppeteer实例
   * @memberof PearsonSpider
   */
  async prepare(cityName){

    await this.init();

    const page = this.page;

    // page.setExtraHTTPHeaders({
    //   "X-FORWARDED-FOR": '124.225.176.82',
    //   "Proxy-Client-IP": '124.225.176.82',
    //   "WL-Proxy-Client-IP": '124.225.176.82',
    //   "HTTP_CLIENT_IP": '124.225.176.82',
    //   "X-Real-IP": '124.225.176.82',
    // })

    await page.goto('https://wsr.pearsonvue.com/testtaker/signin/SignInPage/PEARSONLANGUAGE');
    // 登录
    // await this.type("#SignInForm #inputUserName", 'fuckyouxx');
    // await this.type("#SignInForm #inputPassword", 'FUCKYOUtest123');
    await this.type("#SignInForm #inputUserName", 'wq12345');
    await this.type("#SignInForm #inputPassword", 'ceshiMIMA123../');
    await this.click("#SignInForm #submitButton");
    // Exam Catalogue
    await this.click('#availableExams ul li:first-child a');
    // next
    await this.click('#nextButton');
    const radios = [
        'component1_SELECT_ONE_RADIOBUTTON_3422',
    ];
    const inputs = [{
        id: 'component1_TEXT_3394',
        value: '34234'
    }];
    const selects = [{
        id: 'component1_SELECT_ONE_LISTBOX_2945',
        value: 'YUE'
    }, {
        id: 'component1_SELECT_ONE_LISTBOX_3858',
        value: 'Internet search'
    }, {
        id: 'component1_SELECT_ONE_LISTBOX_4560',
        value: 'My own country'
    }, {
        id: 'component1_SELECT_ONE_LISTBOX_3860',
        value: 'Study'
    }, {
        id: 'component1_SELECT_ONE_LISTBOX_3862',
        value: 'Not Studying'
    }, {
        id: 'component1_SELECT_ONE_LISTBOX_4567',
        value: 'Not Studying'
    }, {
        id: 'component1_SELECT_ONE_LISTBOX_5155',
        value: 'No'
    }];

    for (let radio of radios){
        const selector = `input[name='${radio}']`;
        await this.click(selector);
    }

    for (let select of selects){
        const selector = `select#${select.id}`;
        await this.select(selector, select.value);
        const status = await detectRequesting();
    }

    for (let input of inputs){
        const selector = `input#${input.id}`;
        this.type(selector, input.value);
    }

    // 提交表单
    await this.click('#nextButton');

    

    try {
      await this.type('#testCentersNearAddress', cityName);
      // 搜索
      await this.click('#addressSearch');
    } catch (error) {
      // 搜索页面
      const geoInfo = await got(`https://ditu.google.cn/maps/api/geocode/json?language=en-UK&address=${cityName}&key=AIzaSyDSCL2P-emde6kzlSMLTr2YWs009yGKyU4`);

      const address_components = JSON.parse(geoInfo.body).results[0].address_components.reverse();

      const [country, state, city] = address_components.map(addr => addr.long_name);

      console.log(country, state, city);

      await this.waitForSelector('#country');
      console.log(111);
      const countryValue = await this.page.evaluate(country => {
        for (let item of document.querySelectorAll('#country option')){
          if(item.innerHTML.trim() === country){
            return item.value;
          }
        }
      }, country);
      await this.select('#country', countryValue);
      await this.waitForSelector('#state');
      const stateValue = await this.page.evaluate(state => {
        for (let item of document.querySelectorAll('#state option')){
          if(item.innerHTML.trim() === state){
            return item.value;
          }
        }
      }, state);
      console.log(stateValue, 'state');
      await this.select('#state', stateValue);
      await this.waitForSelector('#city');
      await this.page.evaluate(city => {
        document.querySelector('#city').value = city;
      }, city);
      await this.click('#Search');
    }
  }

  /**
   * 获取考点列表
   */
  async getSearchList(){
    const dataSelector = '#centerTable tbody tr';
    await this.waitForSelector(dataSelector);
    try {
      await this.page.waitFor(dataSelector => document.querySelector(dataSelector).length > 1, {
        timeout: 2500
      }, dataSelector);
    } catch (error) {
      await this.page.waitFor(1000);
    }
    const results = await this.page.evaluate(selector => {
      const lists = document.querySelectorAll(selector);
      return Array.from(lists).map((list, i) => {
        return {
          id: list.querySelector(`#testCenter_${i} input[type='checkbox']`).value,
          title: list.querySelector('.tc_name').innerText,
          address: list.querySelector('.tc_address').innerText,
          href: list.querySelector('.tc_info a').href
        };
      });
    }, dataSelector);
    console.log(results);
  }

  /**
   * 到日期页面
   * @param {string} id 考点id
   */
  async gotoSearchDatePage(testCenterId){
    const id = testCenterId + '';
    await this.click(`#centerTable input[value="${id}"]`);
    await this.click('input.btn[value="Next"][type="submit"]');
    // await this.waitForSelector('.ui-datepicker-calendar td[data-event="click"]');
    await this.waitForSelector('.ui-datepicker-calendar td');
  }

  /**
   * 获取当前页面可用日期
   */
  async getResultDates(){
    const resList = await this.page.evaluate(() => {
      const dates = document.querySelectorAll('.ui-datepicker-calendar td[data-event="click"]');
      return Array.from(dates).map(date => {
        return {
          year: date.getAttribute('data-year'),
          month: String(+date.getAttribute('data-month') + 1),
          day: date.querySelector('a').innerText
        };
      });
    });
    return resList;
  }

  /**
   * 获取最近可用日期
   * @param {string} testCenterId 考点id
   */
  async getSearchDate(testCenterId){
    await this.gotoSearchDatePage(testCenterId);
    let results = [];

    for(;;){
      const className = await this.page.$eval('#inAccessibleCalendar .ui-datepicker-next', btn => btn.className);
      console.log(className);
      const hasNext = !className.includes('ui-state-disabled');
      const resList = await this.getResultDates();
      results = results.concat(resList);
      if(hasNext){
        console.log('has next');
        await this.click('#inAccessibleCalendar .ui-datepicker-next');
        console.log('clicked');
        await this.page.waitForResponse(res => {
          return res.url().includes(`CalendarAppointmentSearchPage/PEARSONLANGUAGE/`);
        }, {timeout: 2000});
        console.log('get next...');
      }else{
        break
      }
    }

    // 去重
    let newArr = [];
    for(date of results){
      if(newArr.find(d => (
        d.year === date.year &&
        d.month === date.month && 
        d.day === date.day
      ))){
        continue;
      }
      newArr.push(date);
    }
    console.log(newArr);
  }

  /**
   * 获取某天的日期
   * @param {number|string} testCenterId 考点id
   * @param {object} searchDate 日期
   * @example getSearchTimes(50487, {
   *  year: '2018',
   *  month: 10,
   *  day: 23
   * })
   */
  async getSearchTimes(testCenterId, {year, month, day}){
    await this.gotoSearchDatePage(testCenterId);
    
    while(true){
      await this.waitForSelector('#inAccessibleCalendar .ui-datepicker-next');

      const className = await this.page.$eval('#inAccessibleCalendar .ui-datepicker-next', btn => btn.className);

      console.log(className);
      
      const hasNext = !className.includes('ui-state-disabled');

      console.log(hasNext);

      const avaDates = await this.getResultDates();

      console.log(avaDates);
      for (let i = 0; i < avaDates.length; i++){
        const date = avaDates[i];
        console.log(date);
        if(String(date.year) === String(year) && String(date.month) === String(month) && String(date.day) === String(day)){
          console.log('matched', date);
          await this.click(`.ui-datepicker-calendar td[data-event="click"]:nth-child(${i+1})`);
          await detectRequesting();
          const times = await this.$$eval('#chooseAppointments input[name="test"]', inps => {
            return inps.map(inp => inp.value);
          });
          console.log(times);
          return times;
        }
      }
      if(hasNext){
        console.log(hasNext);
        await this.waitForSelector('#inAccessibleCalendar .ui-datepicker-next');
        await this.click('#inAccessibleCalendar .ui-datepicker-next');
        await detectRequesting();
      }else{
        console.log('break');
        break;
      }
    }

    
  }
}

const main = async () => {
  const p = new PearsonSpider();
  await p.prepare('Shanghai');
  await p.getSearchList();
  await p.getSearchDate(50487);
  // await p.getSearchTimes(50487, { year: '2018', month: '10', day: '11' },)

  await p.page.deleteCookie();
}

main();