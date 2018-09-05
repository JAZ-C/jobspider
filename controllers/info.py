from flask_restful import Resource, reqparse
from flask import jsonify
from spider import Spider

parser = reqparse.RequestParser()
parser.add_argument('info_id')
parser.add_argument('url')


class Info(Resource):

    def __init__(self):
        self.sp = Spider()

    def get(self, address):
        try:
            rv = self.sp.searchList(address)
            rv["code"] = 200
        except:
            rv = {
                "code": 500,
                "msg": "Get Address List Fail"
            }
        return jsonify(rv)

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
