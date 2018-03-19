"""helpers functions

Those functions aim to make views more readable and maintanable
"""
from collections import OrderedDict
import numpy as np

from alayatodo import app
from flask import (
    session
)
from .models import Todos

MAX_PER_PAGE = app.config['TODO_PER_PAGE']


def model_serializer(model):
    """convert a Model to a dict for session update
    :param SQLALchemy Model instance
    :return OrderedDict
    example: object_serialized = model_serializer(user)
    session['user'] = object_serialized
    """
    result = OrderedDict()
    for key in model.__mapper__.c.keys():
        result[key] = getattr(model, key)

    return result


def url_redirect(is_delete=False, is_create=False, is_update=False):
    """which page to display depends on MAX_PER_PAGE and total records
    user may want to stay on same page after CRUD operations
    for a delete or a create, the user might have to change page depending on pagination
    if only record remains and is deleted, we go back
    if the page is full we go to the next
    :param no params
    :return url to redirect and page in tuple
    """
    todo_total_count = Todos.query.filter_by(user_id=session['user']['id']).count()
    page = int(np.ceil(todo_total_count / np.float(app.config['TODO_PER_PAGE'])))

    number_record_visible = todo_total_count - page * MAX_PER_PAGE
    if is_delete and number_record_visible == 1:
        page-=1
        np.max([page, 1])
    if is_create and number_record_visible % MAX_PER_PAGE == 0:
        page+=1
    url_to_redirect = '/todos/'
    if page > 1:
        url_to_redirect = '/todos/?page={}'.format(page)
    return url_to_redirect
