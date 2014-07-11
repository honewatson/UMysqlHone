__author__ = 'honhon'
from schematics.types.compound import ListType, ModelType
from schematics.models import Model
from schematics.types import StringType, IntType, DateTimeType, URLType


class Link(Model):
    name = StringType()
    slug = StringType()
    url = URLType()

class MenuItem(Link):
    primary = "menu_id"
    menu_id = IntType()

class MenuItemImage(MenuItem):
    image = StringType()

class MenuItemItems(MenuItem):
    block_items = ListType(ModelType(Link))

a = MenuItemItems({"block_items":[{"name": "Item 1"}, {"name": "Item 2"}]})

a.validate()

print a.to_primitive()

class MenuItems(Model):
    menu_items = ListType(ModelType(MenuItem))

f = MenuItem({"name":"Polly"})

g = MenuItemImage({"name":"Dolly"})

m = MenuItems()

m.menu_items = [f, g]

m.menu_items.append(f)

print f.to_primitive()

m.validate()

print m.to_primitive()

x = MenuItems()