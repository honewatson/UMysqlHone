SCHEMA_CACHE = {}
CLASS_PROPERTIES_CACHE = {}
ATTRIBUTE_REMOVES = ['__module__', '__doc__']

from entities import Attribute, Model

def class_properties(ob, callback = lambda ob, property: True):
    return [
        property
        for property in ob.__class__.__dict__.keys()
        if property not in ATTRIBUTE_REMOVES and callback(ob, property)
    ]
    #l.reverse()
    #return l

def schema(ob, callback):

    def attribute(property, ob):
        if isinstance(getattr(ob, property), Attribute):
            return type(getattr(ob, property))

    def model(property, ob):
        return schema(getattr(ob, property), callback)

    attributes = {
        property: attribute(property, ob) or model(property, ob)
        for property in class_properties(ob, callback)
    }

    return {
        "attributes": attributes,
        "entity": type(ob).__name__
    }


def is_attribute_or_model(ob, property):
    prop = getattr(ob, property)
    return isinstance(prop, Attribute) or isinstance(prop, Model)


def class_properties_cache(ob, callback = lambda ob, property: True):
    name = type(ob).__name__
    if CLASS_PROPERTIES_CACHE.get(name, ""):
        return CLASS_PROPERTIES_CACHE.get(name, "")
    CLASS_PROPERTIES_CACHE[name] = cls_properties = class_properties(ob, callback)
    return cls_properties

def schema_cache(ob, callback = lambda ob, property: True):
    name = type(ob).__name__
    if SCHEMA_CACHE.get(name, ""):
        return SCHEMA_CACHE.get(name, "")
    SCHEMA_CACHE[name] = _schema = schema(ob, callback)
    return _schema

_DIR = dir(object)

def basic_all_properties(ob, callback):
    _ob = dir(ob)
    return {
        property: getattr(ob, property)
        for property in _ob
        if property not in _DIR and callback(ob, property)
    }

def all_objects(cls):
    c = [cls]
    if cls.__bases__:
        for x in cls.__bases__:
            if x.__name__ not in ("Model", "object"):
                if x.__bases__:
                    for  y in all_objects(x):
                        c.append(y)
                else:
                    c.append(x)
    return c


class Query(object):

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

query = Query()