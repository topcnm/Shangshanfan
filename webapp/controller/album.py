# coding=utf-8
from PIL import Image
from flask import Blueprint, request, render_template, url_for, session, abort
from webapp.extension import db
from webapp.model import Picture, Album, Tag, Author
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
    photo_path_arr = []

    if len(images) > 5:
        return upload_res_factory(
            errno=1,
            message=u'一次上传太多图片',
        )

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

            mini_ref_file_path = '/static/store/{filename}_mini.{appendix}'.format(
                filename=file_name,
                appendix=image_type
            )

            # abs path is for storing image
            abs_file_path = '{folder}/{filename}.{appendix}'.format(
                folder=store_path,
                filename=file_name,
                appendix=image_type
            )

            # min abs path for compressed image
            mini_abs_file_path = '{folder}/{filename}_mini.{appendix}'.format(
                folder=store_path,
                filename=file_name,
                appendix=image_type
            )

            try:
                # save raw picture, SAVE RAW PICTURE MUST COME FIRST!!!
                image.save(abs_file_path)

                # save compressed picture, special manipulate 'jpg'
                mini_image = Image.open(image, mode='r')

                # manipulate size of image
                width, height = mini_image.size

                # resize picture
                img_scale = min(width/320, height/220)

                mini_image_output = mini_image.resize(
                    (width/img_scale, height/img_scale),
                    Image.ANTIALIAS
                )
                mini_image_output.save(mini_abs_file_path, image_type)

            except Exception, reason:
                print 1, reason
                continue
            else:
                if os.stat(abs_file_path).st_size > 1600 * 900:  # delete photo if it is too large
                    os.remove(abs_file_path)
                    os.remove(mini_abs_file_path)
                    continue

                picture_orm = Picture(
                    fullLink=ref_file_path,
                    tinyLink=mini_ref_file_path,
                    authorId=session.get('author_id'),
                )

                db.session.add(picture_orm)
                photo_path_arr.append(ref_file_path)
        else:
            continue

    try:
        db.session.commit()
    except Exception, reason:
        for photo in photo_path_arr:  # roll back if commit failed
            os.remove(photo)

        return upload_res_factory(
            errno=1,
            message=reason,
        )
    else:
        return upload_res_factory(
            errno=int(not photo_path_arr),
            data=photo_path_arr,
            message=u'上传失败' if int(not photo_path_arr) else ''
        )


@picture.route('/delete/<int:pictureId>', methods=['get'])
def picture_delete(pictureId):
    picture = Picture.query.filter(Picture.id == pictureId).first()
    if picture and picture.authorId == session['author_id']:
        db.session.delete(picture)
        try:
            db.session.commit()
        except Exception, reason:
            return response_factory(
                success=False,
                message=reason
            )
        else:
            return response_factory()
    else:
        return response_factory(
            success=False,
            message=u'相片不存在'
        )


@picture.route('/migrate', methods=['post'])
# @login_required
def picture_migrate():
    """
    设置相册的归属
    :return:
    """
    album_id = request.form['albumId']
    picture_list = request.form['pictureList']

    print album_id, picture_list
    album = Album.query.filter(
        Album.id == album_id,
        # Album.authorId == session['author_id']
    ).first()
    print type(album_id)
    if album and picture_list:
        picture_id_list = picture_list.split(',')
        print picture_id_list
        Picture.query.filter(
            Picture.id.in_(picture_id_list)
        ).update({
            'albumId': album.id
        }, synchronize_session=False)

        try:
            db.session.commit()
        except Exception, reason:
            return response_factory(
                success=False,
                message=reason
            )
        else:
            return response_factory()

    else:
        return response_factory(
            success=False,
            message=u'相册不存在'
        )


@album.route('/create', methods=['post'])
# @login_required
def album_create():
    title = request.form['title']
    remark = request.form['remark']
    privacy = bool(request.form['privacy'])
    author_id = 1 or session['author_id']
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
        return response_factory(
            success=False,
            message=reason
        )
    else:
        return response_factory(
            data={
                'title': title,
                'tagId': tagId,
                'remark': remark,
                'privacy': privacy,
            }
        )


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
        return response_factory(
            success=False,
            message=reason
        )
    else:
        return response_factory(
            data={
                'title': title,
                'tagId': tagId,
                'remark': remark,
                'privacy': privacy,
            }
        )


@album.route('/delete/<int:albumId>', methods=['get'])
def album_delete(albumId):
    pass


@album.route('/setCover/<int:albumId>/<int:pictureId>', methods=['get'])
def album_set_cover(albumId, pictureId):
    picture = Picture.query.filter(Picture.id == pictureId).first()
    print picture.tinyLink, albumId
    if picture:
        print Album.query.filter(Album.id == albumId).first()
        Album.query.filter(Album.id == albumId).update({
            'cover': picture.tinyLink
        })
        try:
            db.session.commit()
        except Exception, reason:
            return response_factory(
                success=False,
                message=reason
            )
        else:
            return response_factory()

    return response_factory(
        success=False,
        message=u'照片不存在'
    )


@album.route('/setCarrousel/<int:albumId>')
def album_set_carrousel(albumId):
    old_album = Album.query.filter(
        Album.iscarrousel
    ).first()

    new_album = Album.query.filter(
        Album.id == albumId
    ).first()

    if not new_album:
        return response_factory(
            success=False,
            message=u'相册不存在'
        )
    else:
        new_album.iscarrousel = True
        old_album.iscarrousel = False

        try:
            db.session.commit()
        except Exception, reason:
            return response_factory(
                success=False,
                message=reason
            )
        else:
            return response_factory(
                message=u'操作成功'
            )


@album.route('/dashboard', methods=['get'])
def page_album_dashboard():
    # albums = Album.query.all()
    tags = Tag.query.all()

    login_user = None

    if session.get('author_id'):
        login_user = Author.query.filter(Author.id == session['author_id']).first()

    return render_template(
        'gallery.html',
        loginUser=login_user,
        tagArr=tags,
        tagsData=json.dumps([{"title": tag.title, "id": tag.id} for tag in tags])
    )


# 0 for unsort
@album.route('/query/<int:albumId>', methods=['get'])
def page_album_query(albumId):
    albums = Album.query.all()

    login_user = None

    if session.get('author_id'):
        login_user = Author.query.filter(Author.id == session['author_id']).first()

    if albumId is 0:
        pictures = Picture.query.filter(Picture.albumId == None).all()
        print pictures

        return render_template(
            'album-detail.html',
            pictures=pictures,
            albums=albums,
            loginUser=login_user,
        )
    else:
        album = Album.query.filter(Album.id == albumId).first()
        if album:
            pictures = Picture.query.filter(Picture.albumId == albumId).all()
            return render_template(
                'album-detail.html',
                pictures=pictures,
                albums=albums,
                currentAlbum=album,
                loginUser=login_user,
            )

        return abort(404)


