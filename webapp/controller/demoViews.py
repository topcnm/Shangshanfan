# coding=utf-8
from flask import views, Blueprint, render_template
from webapp.model import Author
from webapp.controller.util import login_required

geek = Blueprint('/geek', __name__)


class ShowView(views.View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, id=None):
        """
        dispatch_request 必须实现的方法
        :param id: 传参与函数视图一致
        :return:
        """
        user = Author.query.filter(Author.id == id).first()

        return render_template(
            'showView.html',
            loginUser=user
        )


geek.add_url_rule(
    '/showView/<int:id>',
    view_func=ShowView.as_view('my_show_view'))
