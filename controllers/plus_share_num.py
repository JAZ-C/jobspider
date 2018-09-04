from flask_restful import Resource
from flask import jsonify, abort, request
from database import db
from models.user import User


class PlusShareNum(Resource):

    def get(self):
        openId = request.args["openId"]
        user = User.query.filter_by(openId=openId).first()
        if user is None:
            return jsonify({
              "code": -1,
              "message": '操作失败'
            })
        user.sharedNum = user.sharedNum + 1
        db.session.commit()
        return jsonify({
          "code": 0,
          "message": '操作成功'
        })