__author__ = 'honhon'

from wheezy.core.benchmark import Benchmark

def a():
    "SELECT {fields} \nFROM {main} {joins} {where} {groupby} {having} {orderby} {limit}".format(
        fields="fields",
        main="main",
        joins="joins",
        where="where",
        groupby="groupby",
        having="having",
        orderby="orderby",
        limit="limit"
    )

def b():
    "SELECT %s \nFROM %s %s %s %s %s %s %s" % (
        "fields",
        "main",
        "joins",
        "where",
        "groupby",
        "having",
        "orderby",
        "limit"
    )

p = Benchmark((
    a,
    b
), 100000)

p.report('public')

x = {"a":{"b":{"c":{"d":{"e":"f"}}}}}

y = {"a":"b","c":"d","e":"f"}

def a():
    y.get('e')

def b():
    y['e']

class C(object):

    def __init__(self, x):
        self.x = x

    def one(self):
        self.x

    def two(self):
        getattr(self, "x")

z = C("f")

p = Benchmark((
    a,
    b,
    z.one,
    z.two
), 100000)

p.report('public')

from umysqlhone.modelling import class_properties, class_properties_cache, schema, is_attribute_or_model, schema_cache
from umysqlhone.otbmodels import BlogModel, Model, Blog

b = Blog()
bm = BlogModel()
bmm = "BlogModel"

def j():
    isinstance(bm, BlogModel)

def k():
    bmm == "BlogModel"

def l():
    assert bmm == "BlogModel"

p = Benchmark((
    j,
    k,
    l
), 100000)

p.report('public')

def n():
    x = schema(Blog(), is_attribute_or_model)

def m():
    x = schema_cache(b, is_attribute_or_model)

def o():
    x = class_properties(b, is_attribute_or_model)

def p():
    x = class_properties_cache(b, is_attribute_or_model)



p = Benchmark((
    n,
    m,
    o,
    p
), 100000)
p.report('public')

x = schema_cache(b, is_attribute_or_model)
print x
x = schema_cache(b, is_attribute_or_model)
print x

