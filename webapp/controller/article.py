# coding=utf-8
from flask import Blueprint, request, render_template
from webapp.extension import db
from webapp.model import Article, Tag
from util import response_factory
import json

article = Blueprint('article', __name__)


@article.route("/<int:id>")
def page_article_detail(id):
    article_detail = {
        'id': 12,
        'title': 'Throfs dana Gusyet Satmasy',
        'content': 'Thi is thr first here ;good is better'
    }
    return render_template(
        'blog-detail.html',
        article=article_detail,
    )


@article.route("/post", methods=['get'])
@article.route("/post/<int:id>", methods=['get'])
def page_article_submit(id=0):
    # find all Tags
    tags = Tag.query.all()

    # if id is given, set content
    essay = None
    if id:
        essay = Article.query.filter(Article.id == id).first()

    return render_template(
        'blog-submit.html',
        tags=tags,
        article=essay
    )


@article.route("/post", methods=['post'])
def post_article_submit():
    """
    we have to differentiate auto submit and manually submit
    :return:
    """
    articleId = request.form['articleId']
    title = request.form['title']
    content = request.form['content']
    tagId = request.form['tagId']
    privacy = int(request.form['privacy'])
    print privacy, request.form
    if articleId:
        Article.query.filter(Article.id == articleId).update({
            'title': title,
            'content': content,
            'privacy': privacy,
            'tagId': tagId,
            'cover': '',
        })
    else:
        essay = Article(
            title=title,
            content=content,
            cover='',
            privacy=privacy,
            tagId=tagId,
            authorId=1
        )

        db.session.add(essay)

    try:
        db.session.commit()
    except Exception, reason:
        return response_factory(
            success=False,
            message=reason,
        )

    return json.dumps(response_factory(
        success=True,
        data={
            'articleId': 1
        }
    ))
