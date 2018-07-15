# coding=utf-8
from flask import Blueprint, render_template, session
from webapp.extension import db
from webapp.model import Album, Author

common = Blueprint('common', __name__)


@common.route("/index")
def page_home():
    album = Album.query.filter(Album.iscarrousel).first()

    login_user = None

    if session.get('author_id'):
        login_user = Author.query.filter(
            Author.id == session['author_id']
        ).first()

    return render_template(
        'home.html',
        loginUser=login_user,
        album=album
    )


@common.route("/about")
def page_about():
    pass


@common.route("/faq")
def page_fag():
    pass