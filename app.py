from flask import Flask
from flask_restful import (
  Api, 
  Resource
)
from controllers.login import Login
# from controllers.ielts import Ielts
from controllers.info import Info
app = Flask(__name__)
api = Api(app)

api.add_resource(Login, '/login')
# api.add_resource(Ielts, '/get_ielts_info')
api.add_resource(Info, '/info/<string:address>')

if __name__ == '__main__':
    app.run(debug=True)