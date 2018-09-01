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
        return jsonify(self.sp.searchList(address))

    def post(self):
        args = parser.parse_args()
        info_id = args.get('info_id')
        url = args.get('url')
        return jsonify(self.sp.get_tcinfo(info_id, url))