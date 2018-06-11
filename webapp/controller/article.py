# coding=utf-8
from flask import Blueprint, request, render_template
from webapp.extension import db
from webapp.model import Article, Tag
from util import response_factory
import json

article = Blueprint('article', __name__)


# article or destination sum
@article.route("/dashboard")
def page_article_sum():
    tags = Tag.query.all()
    tag_list = []

    for item in tags:
        articles = []

        for index, article_item in enumerate(item.articles):
            if index > 2:
                break
            articles.append({
                'id': article_item.id,
                'title': article_item.title,
                'createDate': article_item.createDate,
                'cover': article_item.cover,
                'summary': article_item.summary,
            })

        if len(articles):
            tag_list.append({
                'title': item.title,
                'remark': item.remark,
                'articles': articles
            })
    return render_template(
        'blog-dashboard.html',
        topiclist=tag_list
    )


# article list by sort
@article.route("/list/<int:tagId>/<int:pageNo>")
def page_article_list_by_tag(tagId, pageNo):
    # find all Tags
    tags = Tag.query.all()
    tag = Tag.query.filter(Tag.id == tagId).first()

    essay_page = Article.query.filter(Article.tagId == tagId).paginate(pageNo, 10)
    total = essay_page.pages

    recent_article = []

    article_top_3 = Article.query.order_by(Article.createDate.desc()).limit(3)

    for item in article_top_3:
        recent_article.append({
            'id': item.id,
            'title': item.title,
            'summary': item.summary,
            'createDate': item.createDate,
        })

    articles = []

    for item in essay_page.items:
        articles.append({
            'id': item.id,
            'title': item.title,
            'createDate': item.createDate,
            'cover': item.cover,
            'summary': item.summary,
        })

    return render_template(
        'blog-list-tag.html',
        articles=articles,
        total=total,
        pageNo=pageNo,
        tags=tags,
        tag=tag,
        recentArticle=recent_article,
    )


# article details
@article.route("/detail/<int:id>")
def page_article_detail(id):
    # find all Tags
    tags = Tag.query.all()
    recent_article = []

    article_top_3 = Article.query.order_by(Article.createDate.desc()).limit(3)

    for item in article_top_3:
        recent_article.append({
            'id': item.id,
            'title': item.title,
            'summary': item.summary,
            'createDate': item.createDate,
        })

    essay = Article.query.filter(Article.id == id).first()
    return render_template(
        'blog-detail.html',
        article=essay,
        tags=tags,
        recentArticle=recent_article,
    )


# article submit page
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


# article submit api
@article.route("/post", methods=['post'])
def article_submit():
    """
    we have to differentiate auto submit and manually submit
    :return:
    """
    articleId = request.form['articleId']
    title = request.form['title']
    content = request.form['content']
    tagId = request.form['tagId']
    privacy = int(request.form['privacy'])
    cover = request.form['cover']
    summary = request.form['summary']

    if articleId:
        Article.query.filter(Article.id == articleId).update({
            'title': title,
            'content': content,
            'privacy': privacy,
            'tagId': tagId,
            'cover': cover,
            'summary': summary,
        })
    else:
        essay = Article(
            title=title,
            content=content,
            summary=summary,
            cover=cover,
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
            'articleId': articleId or essay.id
        }
    ))
