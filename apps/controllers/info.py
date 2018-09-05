from flask_restful import Resource, reqparse
from flask import jsonify, request
from spider import Spider
from database import db
from models.yasi_info import YasiInfo
from models.user import User

parser = reqparse.RequestParser()
parser.add_argument('info_id')
parser.add_argument('url')


class Info(Resource):

    def __init__(self):
        self.sp = Spider()

    def get(self, address):
        openId = request.args["openId"]
        user = User.query.filter_by(openId=openId).first()
        if user is None:
            return []
        results = YasiInfo.query.filter_by(cityname=address).first()
        if results is None:
            results = self.sp.searchList(address)
            newCity = YasiInfo(
                cityname=address,
                detail=results
            )
            db.session.add(newCity)
            db.session.commit()
            return jsonify(results)
        return jsonify(results.detail)

    def post(self):
        args = parser.parse_args()
        info_id = args.get('info_id')
        url = args.get('url')
        try:
            rv = self.sp.get_tcinfo(info_id, url)
            rv["code"] = 200
        except:
            rv = {
                "code": 500,
                "msg": "Get Address Info fail"
            }
        return jsonify(rv)
