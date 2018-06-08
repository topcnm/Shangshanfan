# coding=utf-8
from flask import Blueprint, request, render_template, url_for
from webapp.extension import db
from webapp.model import Picture
from util import response_factory, upload_res_factory
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

    image = request.files.get('image')
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

        pic = Picture(fullLink=ref_file_path, tinyLink=ref_file_path, authorId=1)

        db.session.add(pic)
        try:
            db.session.commit()
            image.save(abs_file_path)
        except Exception, reason:
            return json.dumps(upload_res_factory(
                errno=1,
                message=reason,
            ))
        else:
            return json.dumps(upload_res_factory(data=[
                ref_file_path
            ]))
    else:
        return json.dumps(upload_res_factory(
            errno=2,
            message=u'file type error',
        ))
