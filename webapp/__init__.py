# coding=utf-8
from flask import Flask
from extension import db, logger
from config import DevConfig, ProConfig


def create_app(config_name):
    app = Flask(__name__)
    # config website
    app.config.from_object(config_name)
    pass

    db.init_app(app)

    return app
