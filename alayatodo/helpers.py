from collections import OrderedDict

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