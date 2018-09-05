from flask_restful import Resource, reqparse
from flask import jsonify, request
from spider import Spider
from apps import db, redis_store
from models.yasi_info import YasiInfo
from models.user import User

parser = reqparse.RequestParser()
parser.add_argument('info_id')
parser.add_argument('url')


class Info(Resource):

    def __init__(self):
        self.sp = Spider()

    def get(self, address):
        # openId = request.args["openId"]
        # user = User.query.filter_by(openId=openId).first()
        # if user is None:
        #     return []
        # results = YasiInfo.query.filter_by(cityname=address).first()

        rv = redis_store.get(address)
        if not rv:
            try:
                results = self.sp.searchList(address)
                redis_store.set(address, results)
                rv = results
                rv["code"] = 200
                # newCity = YasiInfo(
                #     cityname=address,
                #     detail=results
                # )
                # db.session.add(newCity)
                # db.session.commit()
            except:
                rv = {
                    "code": 500,
                    "msg": "Get Address Info List Fail!"
                }
        else:
            rv = {address: eval(rv)}
            rv["code"] = 200
        return jsonify(rv)


    def post(self, address):
        args = parser.parse_args()
        info_id = args.get('info_id')
        url = args.get('url')
        # redis_store.delete(info_id)
        rv = redis_store.get(info_id)
        print(rv)
        if not rv:
            try:
                rv = self.sp.get_tcinfo(info_id, url)
                redis_store.set(info_id, rv)
                rv["code"] = 200
            except Exception as e:
                print(e)
                rv = {
                    "code": 500,
                    "msg": "Get Address Info fail"
                }
        else:
            rv = eval(rv)
            rv["code"] = 200
        return jsonify(rv)
