# coding=utf-8
from flask_script import Manager
from webapp.extension import db
from webapp.model import Tag


InitManager = Manager()

tags = ['美丽成都', '小城铜梁', '江南诸暨', '旅行日记']


@InitManager.command
def init_tag():
    for tag_name in tags:
        db.session.add(Tag(title=tag_name))
    db.session.commit()
