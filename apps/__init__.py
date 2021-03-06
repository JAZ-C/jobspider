from flask_migrate import (
  Migrate
)
from flask_restful import (
  Api
)
from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from config import Config



redis_store = FlaskRedis()
api = Api()
migrate = Migrate()

# def creat_app():
app = Flask(__name__, static_folder='../static')

app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store.init_app(app, decode_responses=True)
migrate.init_app(app, db)


from apps.controllers.login import Login
from apps.controllers.plus_share_num import PlusShareNum
from apps.controllers.info import Info
api.add_resource(Login, '/login')
api.add_resource(PlusShareNum, '/update_share_num')
api.add_resource(Info, '/info/<string:address>')
api.init_app(app)




