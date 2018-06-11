# coding=utf-8
from flask import session, request, Blueprint, render_template
from webapp.extension import db, logger
from webapp.model import Author
from util import response_factory, record_operation, login_required
import json


author = Blueprint('author', __name__)


@author.route("/login", methods=['get'])
def page_author_login():
    return render_template(
        'login.html'
    )


@author.route("/login", methods=['post'])
def author_login():
    username = request.form['username']
    password = request.form['password']

    author = Author.get_author_by_username_and_password(username, password)

    if author:
        session['author_id'] = author.id
        session['author_name'] = author.nickname

        return json.dumps(render_template(
            data={'id': author.id}
        ))
    else:

        return json.dumps(response_factory(
            success=False,
            message=u'账户或用户名错误'
        ))


@author.route("/logout", methods=['post'])
@login_required
def author_logout():
    session.pop('author_id')
    session.pop('author_name')

    return json.dumps(response_factory(
        message=u'登出成功'
    ))


@author.route("/register", methods=['get'])
def page_author_register():
    return render_template(
        'register.html'
    )


@author.route("/register", methods=['post'])
def author_register():
    username = request.form['username']
    password = request.form['password']
    repeat_password = request.form['repeat_password']

    if password is not repeat_password:
        return json.dumps(response_factory(
            success=False,
            message=u'密码重复不一致'
        ))

    author = Author(username=username)
    author.set_password(password)

    db.session.add(author)

    try:
        db.session.commit()
    except Exception, reason:
        return json.dumps(response_factory(
            success=False,
            message=reason
        ))

    return json.dumps(response_factory(
        data={'id': author.id}
    ))


@author.route("/update", methods=['post'])
@login_required
def author_update():
    author_id = session['author_id']
    nickname = request.form['nickname']
    portrait = request.form['portrait']
    description = request.form['description']

    try:
        Author.query.filter(Author.id == author_id).update({
            'nickname': nickname,
            'portrait': portrait,
            'description': description,
        })
        db.session.commit()
    except Exception, reason:
        return json.dumps(response_factory(
            success=False,
            message=reason
        ))

    return json.dumps(response_factory(
        data={'id': author_id}
    ))


@author.route("/index", methods=['get'])
@login_required
def page_author_update():
    return render_template(
        'author-center.html'
    )

