class PageModel(object):
    pass


class Attribute(object):
    pass

class IntAttr(Attribute):
    pass

class StringAttr(Attribute):
    validator = ["monkey"]

class Model(object):
    pass

class InvertedIndex(Model):
    pass


class Tag(Model):
    tag_id = IntAttr()
    name = StringAttr()

class Tags(InvertedIndex):
    model = Tag()
    
class BlogModel(Model):
    name = StringAttr()
    tags = Tags()
    pass

class Menu(Model):
    pass

class Footer(Model):
    pass


class Blog(PageModel):
    main = BlogModel()
    menu = Menu()
    footer = Footer()

#/blog/tags/games/21/ = Blog.main.tags where tag_id = 21

class Book(Model):
    name = StringAttr()

b = Book()
b.name = "Spring"

print b.name
print b.__class__.name

class BookShelf(Model):
    other = "monkey"
    colour = StringAttr()
    book = Book()

class Room(Model):
    funny = "joke"
    fireplace = StringAttr()
    bookshelf = BookShelf()

o = object.__dict__.keys()
# print o

a = Attribute.__dict__.keys()

#print a

s = StringAttr.__dict__.keys()
# print s

#print s

n = StringAttr()
n.monkey = "Blue"

SCHEMA_CACHE = {}

ATTRIBUTE_REMOVES = ['__module__', '__doc__']


def class_properties(ob, callback = lambda ob, property: True):
    return [
        property
        for property in ob.__class__.__dict__.keys()
        if property not in ATTRIBUTE_REMOVES and callback(ob, property)
    ]

def  schema(ob, callback):

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


def  is_attribute_or_model(ob, property):
    prop = getattr(ob, property)
    return isinstance(prop, Attribute) or isinstance(prop, Model)


def class_properties_cache(ob, callback = lambda ob, property: True):
    name = type(ob).__name__
    if SCHEMA_CACHE.get(name, ""):
        return SCHEMA_CACHE.get(name, "")
    SCHEMA_CACHE[name] = cls_properties = class_properties(ob, callback)
    return cls_properties

print schema(Blog(), is_attribute_or_model)
# print schema(BlogModel(), is_attribute_or_model)
# print class_properties(BlogModel(), is_attribute_or_model)
exit()

bb = BookShelf()

print class_properties(bb)


print class_properties(bb, is_attribute_or_model)

print  schema(bb, is_attribute_or_model)

room = Room()

print schema(room, is_attribute_or_model)

# def clo(ob, callback):




# __author__ = 'hone'
#
# import inspect
#
# class Attribute(object):
#     def __init__(self, **kwargs):
#         self._params = kwargs
#
#     def set(self, k, v):
#         self._params[k] = v
#
#     def params(self):
#         return self._params
#
#     def get(self, k, default = None):
#         return self._params.get(k, default)
#
#     def extend(self, **kwargs):
#         _params = { k:v for k,v in self._params.items()}
#         for k,v in kwargs.items():
#             _params[k] = v
#         return Attribute(**_params)
#
# class ListAttribute(Attribute):
#     pass
#
# class Simple(object):
#     def __init__(self, **kwargs):
#         self._params = kwargs
#         for k, v in kwargs:
#             setattr(self, k, v)
#
#
# IdType = Attribute(
#     dog="Sausage",
#     validation=['pingu'],
#     default=0,
#     public=True
# )
#
# StringType = Attribute(
#     dog="German Shepard",
#     validation=['dingu'],
#     default="",
#     public=True
# )
#
# SlugType = StringType.extend(
#     dog="Beagle",
#     validation=['wingu']
# )
#
# PrimaryType = IdType.extend(
#     cat="enrique",
#     required_on_update=True
# )
#
#
# PasswordType = StringType.extend(
#     public=False
# )
#
# YesNoType = Attribute(default=False, public=True)
#
# print SlugType.params()
#
#
# class EntityInterface(object):
#     def get_validation(self): raise NotImplementedError()
#
#     def get_all(self): raise NotImplementedError()
#
#     def get_new(self): raise NotImplementedError()
#
#     def get_schema(self): raise NotImplementedError()
#
#     def get_props(self):  raise NotImplementedError()
#
#     def build(self): raise NotImplementedError()
#
#
# class Entity(EntityInterface):
#
#     is_entity = True
#
#     def __init__(self):
#         self.props = self.get_props()
#
#     def _is_entity(self, item):
#         return getattr(item, "is_entity", False)
#
#     def get_props(self):
#         props = dir(self)
#         props.reverse()
#         _props = {}
#         for item in props:
#             _item = getattr(self, item, "")
#             if item == '__class__':
#                 continue
#             elif self._is_entity(_item):
#                 _props[item] = _item
#             elif isinstance(_item, Attribute):
#                 _props[item] = _item
#         return _props
#
#
#     def _get_model_method(self, item, param):
#         key = "get_%s" % param
#         try:
#             return getattr(item, key)()
#         except:
#             item = item()
#             return getattr(item, key)()
#
#     def _get_item(self, item, param):
#         if isinstance(item, ListAttribute):
#             model = item.get('model')
#             return [self._get_model_method(model, param)]
#         elif self._is_entity(item):
#             return self._get_model_method(item, param)
#         else:
#             return item.get(param)
#
#     def _get_attributes_with_param(self, param):
#         return {
#             name: self._get_item(item, param)
#             for name, item in self.props.items()
#         }
#
#     def get_validation(self):
#         return self._get_attributes_with_param("validation")
#
#     def get_public(self):
#         public = self._get_attributes_with_param("public")
#         return public
#
#     def get_new(self):
#         _new = {}
#         for name, item in self.props.items():
#             default = self._get_item(item, "default")
#             if default != None:
#                 _new[name] = default
#             else:
#                 _new[name] = None
#         return _new
#
#     def get_default(self):
#         return self.get_new()
#
#
#
# class Tag(Entity):
#     tag_id = PrimaryType
#     tag_name = StringType
#
# class Address(Entity):
#     address_id = PrimaryType
#     animal_id = IdType
#     city = StringType
#     postcode = StringType
#
#
# class Tags(Entity):
#     tags = ListAttribute(model=Tag)
#
# class Animal(Tags):
#     animal_id = PrimaryType
#     name = StringType
#     password = PasswordType
#     debtfree = YesNoType
#     address = Address
#
#
# a = Animal()
#
# print a.is_entity
#
#
# print a.get_props()
#
#
# print a.get_validation()
#
#
# print a.get_public()
# print a.get_new()
# exit()
#
