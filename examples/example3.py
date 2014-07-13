__author__ = 'hone'

from schematics.models import Model
from schematics.types import StringType, DateTimeType, IntType, URLType
from schematics.types.compound import ListType, ModelType

class Tag(Model):
    primary = "tag_id"
    tag_id = IntType()
    tag_name = StringType()
    slug = StringType()

class TagList(Model):
    tags = ListType(ModelType(Tag))

class Product(TagList):
    primary = "product_id"
    models = ['Product', 'TagList']
    product_id = IntType()
    name = StringType()

tag_dict = {"tags": [{"tag_name": "Blue", "slug": "blue"},{"tag_name": "Red", "slug": "red"}]}

tags = TagList(
    tag_dict
)

p1 = Product({
    "name": "Bloom T-Shirt",
    "tags": tags.tags
})

# print p1.to_primitive()

p2 = Product({
    "name":  "Nirvana T-Shirt",
    "tags": tag_dict['tags']
})

# print p2.to_primitive()
#
# print p2.keys()
#
# print p2.tags
#
# print type(p1).__name__



def print_ob(ob):
    results = dir(ob)
    for i in results:
        print "\n\n"
        print i
        at = getattr(ob, i, "")
        if callable(at):
            try:
                print at()
            except Exception, e:
                print e
        else:
            try:
                print at
            except Exception, e:
                print e

def get_all_fields(ob):
    def field(k, v):
        name = type(v).__name__
        if name == "ListType":
            return { k: get_all_fields(v.model_class)  }
        else: return {k: name }

    fields = [ field(k,v) for k,v in ob._fields.iteritems()]
    return fields

#print get_all_fields(p1)

#print_ob()

#print_ob(p1.name)

#print getattr(p1.name, "__class__")

#print p1.name.__class__.__name__

print p1.tags

class Tables(object):

    def __init__(self, types, main = None):
        self.types = types
        self.main = None

    def get_table(self, model, table):
        if self.main == None:
            if type(model).__name__ == table:
                self.main = Model.to_primitive()

            else:
                raise Exception("The main model should be listed first in the models and should be the same name as the model")




    def list(self, model):
        self.main = None
        tables = [self.get_table(model, table) for table in model.models]
        return tables

#t = Tables()

#print type(t).__name__