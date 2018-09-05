from flask_script import Manager
from flask_migrate import (
  Migrate,
  MigrateCommand
)
from flask_restful import (
  Api, 
  Resource
)
from application import app
from database import db
from controllers.login import Login
from controllers.plus_share_num import PlusShareNum
from controllers.info import Info

manager = Manager(app)

migrate = Migrate(app,db)

api = Api(app)

manager.add_command('db',MigrateCommand)

api.add_resource(Login, '/login')
api.add_resource(PlusShareNum, '/update_share_num')
api.add_resource(Info, '/info/<string:address>')

if __name__ == '__main__':
    manager.run()