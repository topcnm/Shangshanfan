# coding=utf-8
from extension import db, bcrypt
import datetime


class Utf8Set(object):
    __table_args__ = {
        'mysql_charset': 'utf8'
    }


class Author(db.Model, Utf8Set):
    """
    Every author has the right to edition in principle,
    However this functionality is only for website manager apparently.
    What was lucky, submitting a comment is available for all users;
    """
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(64), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    portrait = db.Column(db.String(128))
    description = db.Column(db.String(512), default=u'This Guy is lazy enough! oops')

    # one to many
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    albums = db.relationship('Album', backref='author', lazy='dynamic')
    pictures = db.relationship('Picture', backref='author', lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_author_by_username_and_password(username, password):
        author = Author.query.filter(Article.username == username).first()
        if author:
            if author.check_password(password):
                return author
            else:
                return None
        else:
            return None


class Article(db.Model, Utf8Set):
    """
        For article detail
        article info: id \ title \ text\ create_date \ update_date
        access  info: privacy\status
    """
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    cover = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(255), default=u'作者还未添加文字信息')

    # default value is draft and public
    status = db.Column(db.Boolean, default=False)
    privacy = db.Column(db.Boolean, default=False)
    createDate = db.Column(db.DateTime, default=datetime.datetime.now)
    updateDate = db.Column(db.DateTime, default=datetime.datetime.now)

    # one to one
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'))
    # travel \ dairy, or blog articles are belong to dairy
    # 'My life' 'Beautiful Chengdu' 'Small City Tongliang' 'Hometown Zhuji'
    tagId = db.Column(db.Integer, db.ForeignKey('tag.id'))

    # one to many
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def __init__(self, title, content, summary, privacy, tagId, authorId, cover=''):
        self.title = title
        self.content = content
        self.summary = summary
        self.privacy = privacy
        self.cover = cover
        self.tagId = tagId
        self.authorId = authorId


class Tag(db.Model, Utf8Set):
    """
    'My life'
    'Beautiful Chengdu'
    'Small City Tongliang'
    'Hometown Zhuji'
    """
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    remark = db.Column(db.String(255), default=u'No introduction for tag')

    albums = db.relationship('Album', backref='tag', lazy='dynamic')
    articles = db.relationship('Article', backref='tag', lazy='dynamic')


class Destination(db.Model, Utf8Set):
    """
    Cities
    """
    __tablename__ = 'destination'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    remark = db.Column(db.String(255))


class Comment(db.Model, Utf8Set):
    """
    to who
    """
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    createDate = db.Column(db.DateTime, default=datetime.datetime.now)

    # one to one
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'))
    articleId = db.Column(db.Integer, db.ForeignKey('article.id'))
    # toWhoId = db.Column(db.Integer, db.ForeignKey('author.id'))

    # **Important:cause we have set multiple foreign key which refers to the same table `author`
    # so we have to attach relationship and specify the foreign key
    # author = db.relationship('Author', foreign_keys=[authorId])
    # toWho = db.relationship('Author', foreign_keys=[toWhoId])


class Album(db.Model, Utf8Set):
    """
    All albums are public;
    Currently, Album refer to tag
    Dairy
        Emotion
        Capture
    Travel
        ChengDu
        Tongliang
        Zhuji
    """
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    remark = db.Column(db.String(255), nullable=False)
    cover = db.Column(db.String(255), nullable=False)

    privacy = db.Column(db.Boolean, default=False)
    createDate = db.Column(db.DateTime, default=datetime.datetime.now)

    # one to one
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'))
    tagId = db.Column(db.Integer, db.ForeignKey('tag.id'))

    # one to many
    pictures = db.relationship('Picture', backref='album', lazy='dynamic')


class Picture(db.Model, Utf8Set):
    """
    All pictures are public,
    Also portraits are include
    """
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    remark = db.Column(db.String(255), default=u'the owner was lazy and left nothing')

    # In the near future , we may save the pics by two resolutions
    # one is for list, another is for detail
    fullLink = db.Column(db.String(255))
    tinyLink = db.Column(db.String(255))
    uploadDate = db.Column(db.DateTime, default=datetime.datetime.now)
    albumId = db.Column(db.Integer, db.ForeignKey('album.id'))
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __init__(self, fullLink, tinyLink, authorId):
        self.fullLink = fullLink
        self.tinyLink = tinyLink
        self.authorId = authorId
