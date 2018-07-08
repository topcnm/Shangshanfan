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

        return response_factory(
            data={'id': author.id}
        )
    else:

        return response_factory(
            success=False,
            message=u'账户或用户名错误'
        )


@login_required
@author.route("/logout", methods=['post'])
def author_logout():
    session.pop('author_id')
    session.pop('author_name')

    return response_factory(
        message=u'登出成功'
    )


@author.route("/register", methods=['get', 'post'])
def page_author_register():
    if request.method == 'GET':
        return render_template(
            'register.html'
        )
    else:
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeatPassword']
        nickname = request.form['nickname']

        exist_author = Author.query.filter(Author.username == username).first()

        if password != repeat_password or exist_author:
            return render_template(
                'register.html',
                username=username,
                nickname=nickname,
                error=response_factory(
                    success=False,
                    message=u'用户已存在' if exist_author else u'密码不一致'
                )
            )

        author = Author(username=username)
        author.set_password(password)
        author.nickname = nickname

        db.session.add(author)

        try:
            db.session.commit()
        except Exception, reason:
            return render_template(
                'register.html',
                username=username,
                nickname=nickname,
                error=response_factory(
                    success=False,
                    message=reason
                )
            )
        else:
            # directly login in
            # session['author_id'] = author.id
            return response_factory(
                data={'id': author.id}
            )


@login_required
@author.route("/update", methods=['post'])
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
        return response_factory(
            success=False,
            message=reason
        )

    return response_factory(
        data={'id': author_id}
    )


@login_required
@author.route("/index", methods=['get'])
def page_author_update():
    return render_template(
        'author-center.html'
    )

