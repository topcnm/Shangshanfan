# coding=utf-8
from flask import Flask, render_template
from extension import db, bcrypt, logger
from config import DevConfig, ProConfig
from controller.article import article
from controller.album import picture, album


def create_app(config_name):
    app = Flask(__name__)
    # config website
    app.config.from_object(config_name)
    pass

    db.init_app(app)
    bcrypt.init_app(app)

    @app.errorhandler(404)
    def page_not_found(err):
        return render_template('404.html'), 404

    # register blueprint, add url
    app.register_blueprint(article, url_prefix='/shangshanfan/article')
    app.register_blueprint(picture, url_prefix='/shangshanfan/picture')
    app.register_blueprint(album, url_prefix='/shangshanfan/album')

    return app
