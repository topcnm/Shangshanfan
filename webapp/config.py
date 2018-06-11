# coding=utf-8
class Config(object):
    pass


class ProConfig(Config):
    DEBUG = False
    SECRET_KEY = 'Life is good'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        'root', '123456', 'localhost', '3306', 'shangshanfan')


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = 'Ok we are Ok'
    # MAX_CONTENT_LENGTH = 1600 * 900
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        'root', '123456', 'localhost', '3306', 'shangshanfan')