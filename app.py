from flask import Flask
from flask_restful import (
  Api, 
  Resource
)
from controllers.login import Login
from controllers.ielts import Ielts
app = Flask(__name__)
api = Api(app)

api.add_resource(Login, '/get_openid')
api.add_resource(Ielts, '/get_ielts_info')

if __name__ == '__main__':
    app.run(debug=True)