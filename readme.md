# Pearson 爬虫

## 文件目录说明

* apps/ -- api接口
* front/ -- 小程序端
* models/ -- 模型定义
* static/ -- 资源目录(用来存放小程序前端的二维码等信息)
* js/ -- 使用nodejs模拟浏览器进行数据访问
* config.py -- 配置
* create_db.py -- 创建数据表
* ipproxy.py -- 代理ip工具
* manage.py -- 启动api服务
* jobspider_nginx.conf -- nginx配置文件
* traffic_monitor_uwsgi.ini -- uwsgi配置文件

## 技术栈
* 后端 python, flask, sqlalchemy, requets, BeautifulSoup
* 小程序 Taro.js

## 爬虫工作流程
1. 获取首页
2. 登录 
3. 搜索页之前的表单填写
4. 搜索考点, 获取考点列表
5. 考点可用日期
6. 考点下每天的具体考试时间


## 遇到问题
1. 到目前这一版本, 获取考点列表已经正常工作
2. 从考位列表到考位具体可用日期页面, 爬虫提交数据后会被无限重定向, 原因暂时无解
3. 如果2能够解决, 考点可用日期以及考点的具体时间数据理论上也能正常工作
4. 获取考点日期及时间更换了数据交换方式, 之前是`json`现在是`xml`
5. 模拟浏览器进行数据访问时, 代理需要支持`http`以及`https`
6. 网站还在升级, 不定时挂掉

## 需要注意的点
1. pearson网站采用分步提交表单, 一定严格注意表单提交流程(我们的方案是使用`requests`提供的`session`工具)
2. 连续请求大概`30`次以上会封ip, 可参考`requests`的`proxy`
3. 由于我们使用的ip是免费ip, 稳定性欠佳, 且分步地域不同, 账号容易被封
4. 注意`request header`中的`referer`和`ua`