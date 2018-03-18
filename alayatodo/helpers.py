import numpy as np

from alayatodo import app
from collections import OrderedDict
from .models import todos
from flask import (
    session
)

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

def url_and_page_redirect():
    """which page to display depends on MAX_PER_PAGE and total records
    user may want to stay on same page after CRUD operations
    :param no params
    :return url to redirect and page in tuple
    """
    todo_total_count = todos.query.filter_by(user_id=session['user']['id']).count()
    page = int(np.ceil(todo_total_count / app.config['TODO_PER_PAGE']))
    url_to_redirect = '/todos/'
    if page > 1:
        url_to_redirect = '/todos/?page={}'.format(page)
    return (url_to_redirect, page)
