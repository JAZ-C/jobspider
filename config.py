import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1432@localhost/yasi_db?charset=utf8"
    REDIS_URL = "redis://:Aa123456@127.0.0.1:6379/0"
    APPID = os.environ.get('APPID') or "wx921250119ac23d41"
    APPSECRET = os.environ.get('APPSECRET') or "b4a51c062575232bd88f82a2b5a3df6b"
