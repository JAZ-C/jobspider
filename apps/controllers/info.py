from flask_restful import Resource, reqparse
from flask import jsonify, request
from spider import Spider
from apps import db, redis_store
from models.user import User

parser = reqparse.RequestParser()
parser.add_argument('info_id')
parser.add_argument('search_month')
parser.add_argument('search_year')
parser.add_argument('search_datetime')



class Info(Resource):

    def __init__(self):
        self.sp = Spider()

    def get(self, address):
        openId = request.args["openId"]
        user = User.query.filter_by(openId=openId).first()
        if user is None:
            return []
        rv = redis_store.get(address)
        if not rv:
            try:
                results = self.sp.doSearchData(address)
                redis_store.set(address, results)
                redis_store.expire(address, 1296000) #设置过期时间为15天
                rv = {address: results}
                rv["code"] = 200
                # user.sharedNum = (user.sharedNum - 1) if user.sharedNum > 1 else 0
                # db.session.add(user)
                # db.session.commit()
            except Exception as e:
                print(e)
                rv = {
                    "code": 500,
                    "msg": "Get Address Info List Fail!"
                }
        else:
            rv = {address: eval(rv)}
            rv["code"] = 200
        return jsonify(rv)

    def post(self, address):
        """
        :param address: 搜索城市
        post的数据
        info_id：选择的地址ID  "info_id: 50488"
        search_month：搜索的月份  "search_month: 10"
        search_year: 搜索的年份  "search_year: 2018"
        search_datetime: 搜索的日期，当需要查询某一天的具体时间的时候才传入这个字段的数据，其他时候不传，该数据的月份年份需与
                    search_month，search_year相同 "search_datetime: 10/16/2018"
        :return:
            如果有search_datetime这个字段, 则返回当日可用时间:["09:00 AM", "12:00 PM", "03:00 PM"]
            如果没有，则返回当月可选日期 ['10/11/2018', '10/13/2018', '10/16/2018', '10/17/2018', '10/20/2018',
            '10/29/2018', '11/01/2018', '11/05/2018', '11/08/2018', '11/15/2018', '11/22/2018', '11/29/2018']
        """
        args = parser.parse_args()
        info_id = args.get('info_id')
        search_month = args.get('search_month')
        search_year = args.get('search_year')
        search_datetime = args.get('search_datetime')
        search_data = dict(zip(['id', 'month', 'year', 'datetime'],
                               [info_id, search_month, search_year, search_datetime]))
        redis_key = address + info_id + "_" + search_month+ "_" + search_year if not search_datetime \
            else address + info_id + "_" + search_datetime
        rv = redis_store.get(redis_key)
        code = 200
        if not rv:
            try:
                rv = self.sp.doSearchData(address, search_data)
                redis_store.set(redis_key, rv)
                redis_store.expire(redis_key, 1296000) #设置过期时间为15天
            except Exception as e:
                print(e)
                code = 500
                rv = []
        else:
            rv = eval(rv)
        return jsonify({
            "code": code,
            "data": rv
        })
