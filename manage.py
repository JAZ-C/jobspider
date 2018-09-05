from flask_script import Manager
from flask_migrate import (
  MigrateCommand
)
from apps import  app

# app = creat_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#
# app = Flask(__name__)
# app.config.from_object(Config)
# manager = Manager(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app,db)
# redis_store = FlaskRedis(app)
# api = Api(app)
#
# manager.add_command('db',MigrateCommand)
#
# api.add_resource(Login, '/login')
# api.add_resource(PlusShareNum, '/update_share_num')
# api.add_resource(Info, '/info/<string:address>')

if __name__ == '__main__':
    manager.run()