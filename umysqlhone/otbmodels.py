__author__ = 'hone'

from modelling import *
from entities import *
from collections import namedtuple

class Tag(Model):
    id = PrimaryAttr()
    name = StringAttr()

class Author(Model):
    id = PrimarySmallAttr()
    name = StringAttr()

class Tags(InvertedIndex):
    model = Tag()

class SmallLinks(Model):
    title = StringAttr()
    sub_title = StringAttr()
    slug = StringAttr()
    url = StringAttr()
    image = StringAttr()
    read_more = StringAttr()

class Mello(Model):
    mello = StringAttr()

class Hello(Mello):
    hello = StringAttr()

class BlogModel(SmallLinks, Hello):
    blog_id = PrimarySmallAttr()
    author = Author()
    tags = Tags()
    published_date = StringAttr()
    pass

#Only id selects are allowed

result = {
    "blog_id": {
        "sql": "SELECT at_blog_id.blog_id, at_blog_id.author_name, at_blog_id.name FROM blog_model as at_blog_id WHERE at_blog_id = %s",
        "params": ("blog_id",),
        "ntuple": namedtuple("blog_id", "blog_id author_name name")
    },

}

class Menu(Model):
    pass

class Footer(Model):
    pass


class Blog(PageModel):
    main = BlogModel()
    menu = Menu()
    footer = Footer()

# BlogModel = {
#     "tag_name": (InvertedIndex, Tag, "name"),
#     "author_name": (Author, "name"),
#     "blog_id": ("id")
# }
#
# query(BlogModel, blog_id = 21)
# query(BlogModel, tag_name = "Billy")
# query(BlogModel, author_name="Hone")

#/blog/tags/games/21/ = Blog.main.tags where tag_id = 21

class Book(Model):
    name = StringAttr()

b = Book()
b.name = "Spring"

# print b.name
# print b.__class__.name

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



# print schema(Blog(), is_attribute_or_model)
# # print schema(BlogModel(), is_attribute_or_model)
# # print class_properties(BlogModel(), is_attribute_or_model)
#
#
# bb = BookShelf()
#
# print class_properties(bb)
#
#
# print class_properties(bb, is_attribute_or_model)
#
# print  schema(bb, is_attribute_or_model)
#
# room = Room()
#
# print schema(room, is_attribute_or_model)