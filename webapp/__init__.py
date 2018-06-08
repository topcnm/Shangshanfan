# coding=utf-8
from flask import Flask
from extension import db, bcrypt, logger
from config import DevConfig, ProConfig
from controller.article import article
from controller.album import picture


def create_app(config_name):
    app = Flask(__name__)
    # config website
    app.config.from_object(config_name)
    pass

    db.init_app(app)
    bcrypt.init_app(app)

    # register blueprint, add url
    app.register_blueprint(article, url_prefix='/article')
    app.register_blueprint(picture, url_prefix='/picture')

    return app
