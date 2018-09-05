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
from apps.controllers.login import Login
from apps.controllers.plus_share_num import PlusShareNum
from apps.controllers.info import Info

db = SQLAlchemy()
redis_store = FlaskRedis()
api = Api()
migrate = Migrate()

def creat_app():
    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(Config)
        db.init_app(app)
        redis_store.init_app(app)
        migrate.init_app(app, db)
        Api.init_app(app)

        api.add_resource(Login, '/login')
        api.add_resource(PlusShareNum, '/update_share_num')
        api.add_resource(Info, '/info/<string:address>')

        return app



