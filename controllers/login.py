import requests
from flask_restful import Resource, reqparse
from settings import AppId, AppSecret
from flask import jsonify

from database import db
from models.user import User

parser = reqparse.RequestParser()
parser.add_argument('code', type=str)
parser.add_argument('avatarUrl', type=str)
parser.add_argument('city', type=str)
parser.add_argument('country', type=str)
parser.add_argument('gender', type=int)
parser.add_argument('nickName', type=str)
parser.add_argument('province', type=str)

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        code = args['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(
            AppId,
            AppSecret,
            code
        )
        res = requests.post(url).json()
        if not 'openid' in res:
            return jsonify({
                "code": -1,
                "message": '获取ipenid失败',
                "data": res
            })
        openId = res['openid']
        user = User.query.filter_by(openId=openId).first()
        if user is None:
            currentUser = User(
                avatarUrl=args["avatarUrl"],
                city=args["city"],
                country=args["country"],
                gender=args["gender"],
                nickName=args["nickName"],
                province=args["province"],
                openId=openId
            )
            db.session.add(currentUser)
            db.session.commit()
        return jsonify({
            "code": 0,
            "data": openId
        })