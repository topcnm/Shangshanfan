# coding=utf-8
from flask import session, request, Blueprint, render_template, url_for, redirect
from webapp.extension import db, logger
from webapp.model import Author
from util import response_factory, record_operation, login_required
from wtforms import Form, StringField
from wtforms.validators import Length, EqualTo

author = Blueprint('author', __name__, template_folder="../blueprints/author")


class RegisterForm(Form):
    username = StringField(validators=[Length(min=6, max=18, message="username between 6 ~ 18")])
    nickname = StringField(validators=[Length(min=2, max=30, message="nickname between 2 ~ 30")])
    password = StringField(validators=[Length(min=6, max=18, message="password between 6 ~ 18")])
    repeatPassword = StringField(validators=[Length(min=6, max=18, message="repeatPassword between 6 ~ 18"),
                                              EqualTo('password', message="not equals to password")])


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


# @login_required
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
        nickname = request.form['nickname']
        print(request.form)
        form = RegisterForm(request.form)

        if not form.validate():
            return render_template(
                'register.html',
                username=username,
                nickname=nickname,
                error=response_factory(
                    success=False,
                    message=form.errors
                )
            )
        else:
            exist_author = Author.query.filter(Author.username == username).first()

            if exist_author:
                return render_template(
                    'register.html',
                    username=username,
                    nickname=nickname,
                    error=response_factory(
                        success=False,
                        message=u'用户已存在'
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
                session['author_id'] = author.id
                return redirect(url_for("common.page_home"), code=302)


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

