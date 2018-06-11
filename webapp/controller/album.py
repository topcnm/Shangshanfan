# coding=utf-8
from flask import Blueprint, request, render_template, url_for, session, abort
from webapp.extension import db
from webapp.model import Picture, Album, Tag
from util import response_factory, upload_res_factory, login_required
import json
import os
import re
import time
import random
import string


ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']


# check if the file type is ok
def is_allowed_upload(appendix):
    return appendix.lower() in ALLOW_EXTENSIONS


# get the appendix of file
def get_file_appendix(filename):
    result = re.search(r'\.([a-zA-Z]+)', filename)
    if result:
        return result.group(1)
    return result


album = Blueprint('album', __name__)


picture = Blueprint('picture', __name__)


@picture.route('/uploadImage', methods=['post'])
def upload_image():
    basedir = os.getcwd()
    store_path = '{}/webapp/static/store'.format(basedir)
    if not os.path.exists(store_path):
        os.mkdir(store_path)

    images = request.files.getlist('image')
    path_arr = []

    if len(images) > 5:
        return json.dumps(upload_res_factory(
            errno=1,
            message=u'一次上传太多图片',
        ))

    for image in images:
        image_type = get_file_appendix(image.filename)

        if is_allowed_upload(image_type):
            # generate an random name
            file_name = time.strftime('%Y%m%d%H%M%S') + ''.join(random.sample(string.letters, 8))

            # ref path is for front_end and database
            ref_file_path = '/static/store/{filename}.{appendix}'.format(
                filename=file_name,
                appendix=image_type
            )

            # abs path is for storing image
            abs_file_path = '{folder}/{filename}.{appendix}'.format(
                folder=store_path,
                filename=file_name,
                appendix=image_type
            )

            # save
            image.save(abs_file_path)

            # if the size of the file is too large, remove it
            if os.stat(abs_file_path).st_size > 1600 * 900:
                os.remove(abs_file_path)
                continue

            pic = Picture(
                fullLink=ref_file_path,
                tinyLink=ref_file_path,
                authorId=1
            )

            db.session.add(pic)

            path_arr.append(ref_file_path)
        else:
            continue

    try:
        db.session.commit()
    except Exception, reason:
        # roll back if commit failed
        for loc in path_arr:
            os.remove(loc)

        return json.dumps(upload_res_factory(
            errno=1,
            message=reason,
        ))
    else:
        len_arr = len(path_arr)
        return json.dumps(upload_res_factory(
            errno=int(not len_arr),
            data=path_arr,
        ))


@picture.route('/delete/<int:pictureId>', methods=['get'])
def picture_delete(pictureId):
    picture = Picture.query.filter(Picture.id == pictureId).first()
    if picture and picture.authorId == session['author_id']:
        db.session.delete(picture)
        try:
            db.session.commit()
        except Exception, reason:
            return json.dumps(response_factory(
                success=False,
                message=reason
            ))
        else:
            return json.dumps(response_factory())
    else:
        return json.dumps(response_factory(
            success=False,
            message=u'相片不存在'
        ))


@picture.route('/migrate', methods=['post'])
@login_required
def picture_migrate():
    """
    设置相册的归属
    :return:
    """
    album_id = request.form['albumId']
    picture_list = request.form['pictureList']

    album = Album.query.filter(
        Album.id == album_id,
        Album.authorId == session['author_id']
    ).first()

    if album and picture_list and album.id is album_id:
        Picture.query.filter(
            Picture.id.in_(
                picture_list.split(','))
        ).update({
            'albumId': album_id
        })

        try:
            db.session.commit()
        except Exception, reason:
            return json.dumps(response_factory(
                success=False,
                message=reason
            ))
        else:
            return json.dumps(response_factory())

    else:
        return json.dumps(response_factory(
            success=False,
            message=u'相册不存在'
        ))


@album.route('/create', methods=['post'])
@login_required
def album_create():
    title = request.form['title']
    remark = request.form['remark']
    privacy = request.form['privacy']
    author_id = session['author_id']
    tagId = request.form['tagId']

    album = Album(
        title=title,
        remark=remark,
        privacy=privacy,
        authorId=author_id,
        tagId=tagId
    )

    db.session.add(album)

    try:
        db.session.commit()
    except Exception, reason:
        return json.dumps(response_factory(
            success=False,
            message=reason
        ))
    else:
        return json.dumps(response_factory(
            data={
                'title': title,
                'tagId': tagId,
                'remark': remark,
                'privacy': privacy,
            }
        ))


@album.route('/update', methods=['post'])
def album_update():
    album_id = request.form['albumId']
    title = request.form['title']
    remark = request.form['remark']
    privacy = request.form['privacy']
    tagId = request.form['tagId']

    Album.query.filter(
        Album.id == album_id,
        Album.authorId == session['author_id']
    ).update({
        'title': title,
        'remark': remark,
        'privacy': privacy,
        'tagId': tagId,
    })

    try:
        db.session.commit()
    except Exception, reason:
        return json.dumps(response_factory(
            success=False,
            message=reason
        ))
    else:
        return json.dumps(response_factory(
            data={
                'title': title,
                'tagId': tagId,
                'remark': remark,
                'privacy': privacy,
            }
        ))


@album.route('/delete/<int:albumId>', methods=['get'])
def album_delete(albumId):
    pass


@album.route('/dashboard', methods=['get'])
def page_album_dashboard():
    albums = Album.query.all()
    tags = Tag.query.all()
    return render_template(
        'gallery.html',
        albums=albums,
        tags=tags
    )


# 0 for unsort
@album.route('/query/<int:albumId>', methods=['get'])
def page_album_query(albumId):
    if albumId is 0:
        pictures = Picture.query.filter(Picture.albumId is None).all()
        return render_template(
            'album-detail.html',
            pictures=pictures
        )
    else:
        album = Album.query.filter(Album.id == albumId)
        if album:
            pictures = Picture.query.filter(Picture.albumId == albumId).all()
            return render_template(
                'album-detail.html',
                pictures=pictures
            )

        return abort(404)


