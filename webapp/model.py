# coding=utf-8
from extension import db


class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
