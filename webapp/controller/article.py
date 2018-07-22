# coding=utf-8
from flask import Blueprint, request, render_template, session, views
from webapp.extension import db
from webapp.model import Article, Tag, Author
from util import response_factory

article = Blueprint('article', __name__, template_folder="../blueprints/post")


# article or destination sum
@article.route("/dashboard")
def page_article_sum():
    tags = Tag.query.all()
    tag_list = []

    login_user = None

    if session.get('author_id'):
        login_user = Author.query.filter(Author.id == session['author_id']).first()

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
        loginUser=login_user,
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

    login_user = None

    if session.get('author_id'):
        login_user = Author.query.filter(Author.id == session['author_id']).first()

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
        loginUser=login_user,
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

    login_user = None

    if session.get('author_id'):
        login_user = Author.query.filter(Author.id == session['author_id']).first()

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
        loginUser=login_user,
        article=essay,
        tags=tags,
        recentArticle=recent_article,
    )


class ArticlePostView(views.View):
    def dispatch_request(self, id=None):
        # find all Tags
        tags = Tag.query.all()

        # if id is given, set content
        essay = Article.query.filter(
            Article.id == id
        ).first()

        login_user = Author.query.filter(
            Author.id == session.get('author_id')
        ).first()

        return render_template(
            'blog-submit.html',
            loginUser=login_user,
            tags=tags,
            article=essay
        )


article.add_url_rule(
    '/post',
    view_func=ArticlePostView.as_view('page_article_create'),
)
article.add_url_rule(
    '/post/<int:id>',
    view_func=ArticlePostView.as_view('page_article_submit')
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

    return response_factory(
        success=True,
        data={
            'articleId': articleId or essay.id
        }
    )
