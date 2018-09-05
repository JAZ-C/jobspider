from flask import Flask
from flask_restful import (
  Api
)
from config import Config
from apps.controllers.login import Login
# from controllers.ielts import Ielts
from apps.controllers.info import Info
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

api.add_resource(Login, '/login')
# api.add_resource(Ielts, '/get_ielts_info')
api.add_resource(Info, '/info/<string:address>')

if __name__ == '__main__':
    app.run(debug=True)