SCHEMA_CACHE = {}

ATTRIBUTE_REMOVES = ['__module__', '__doc__']

from entities import Attribute, Model

def class_properties(ob, callback = lambda ob, property: True):
    return [
        property
        for property in ob.__class__.__dict__.keys()
        if property not in ATTRIBUTE_REMOVES and callback(ob, property)
    ]

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
    if SCHEMA_CACHE.get(name, ""):
        return SCHEMA_CACHE.get(name, "")
    SCHEMA_CACHE[name] = cls_properties = class_properties(ob, callback)
    return cls_properties


class Query(object):

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

query = Query()