import requests
from flask_restful import Resource, reqparse
from settings import AppId, AppSecret

parser = reqparse.RequestParser()
parser.add_argument('code', type=str)
parser.add_argument('username', type=str)
parser.add_argument('avatar', type=str)

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
            return {
                code: -1,
                "message": '获取ipenid失败',
                "data": res
            }
        return {
            code: 0,
            "data": res['openid']
        }