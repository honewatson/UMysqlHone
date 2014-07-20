__author__ = 'honhon'

from umysqlhone.modelling import *

from umysqlhone.otbmodels import BlogModel, SmallLinks

b = BlogModel()

print(schema(b, is_attribute_or_model))

print b.__class__.__bases__[0]

# print dir(b.__class__.__bases__[0])

def is_attribute_or_model(ob, property):
    prop = getattr(ob, property, "")
    return isinstance(prop, Attribute) or isinstance(prop, Model)

def class_properties(ob, callback = lambda ob, property: True):
    return [
        property
        for property in ob.__class__.__dict__.keys()
        if property not in ATTRIBUTE_REMOVES and callback(ob, property)
    ]



# print base_properties(b.__class__.__bases__[0], is_attribute_or_model)

def get_all_properties(ob, callback = lambda ob, property: True):
    def base_properties(ob, callback = lambda ob, property: True):
        return [
            property
            for property in ob.__dict__.keys()
            if property not in ATTRIBUTE_REMOVES and callback(ob, property)
        ]
    first = base_properties(ob, callback)
    for base in ob.__bases__:
        first += get_all_properties(base, callback)
    return first

#bm = [base_properties(_b, is_attribute_or_model) for _b in b.__class__.__bases__]

print(get_all_properties(BlogModel, is_attribute_or_model))

print(dir(object))

print(get_all_properties(SmallLinks, is_attribute_or_model))


print(basic_all_properties(BlogModel, is_attribute_or_model))

def xget_all_properties(ob, callback = lambda ob, property: True):
    def xbase_properties(ob, callback = lambda ob, property: True):
        return [
            property
            for property in ob.__dict__.keys()
            if property not in ATTRIBUTE_REMOVES and callback(ob, property)
        ]
    first = xbase_properties(ob, callback)
    next =  [xget_all_properties(base, callback) for base in ob.__bases__ if base and type(base).__name__ != "object"]
    if next:
        result = first + next
        return result


# print(xget_all_properties(BlogModel, is_attribute_or_model))



# print(all_objects(BlogModel))

obs = all_objects(BlogModel)

print obs

print obs[0].__dict__