import os



class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = ""
    APPID = os.environ.get('APPID') or ""
    APPSECRET = os.environ.get('APPSECRET') or ""