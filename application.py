from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1432@localhost/yasi_db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True