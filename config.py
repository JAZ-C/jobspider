import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1432@localhost/yasi_db?charset=utf8"
    REDIS_URL = "redis://:Aa123456@127.0.0.1:6379/0"
    APPID = os.environ.get('APPID') or "wx58e87ebc44b74632"
    APPSECRET = os.environ.get('APPSECRET') or "154be445da85d56ae984c84ace9487b8"
