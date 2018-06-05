# coding=utf-8
import sys
from flask import abort, session
sys.path.append('../')
from extension import logger


def login_required(func):
    def wrapped_func(*kw, **kwargs):
        if 'user_id' in session:
            return func(*kw, **kwargs)
        else:
            return abort(401)

    return wrapped_func


def record_operation(func):
    def wrapped_func(*kw, **kwargs):
        logger.info("{}, params1: {}; params2: {}".format(func.__name__, kw, kwargs))
        return func(*kw, **kwargs)

    return wrapped_func

