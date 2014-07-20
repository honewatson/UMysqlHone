__author__ = 'honhon'

from collections import namedtuple

class A(object):
    def __init__(self, tup):
        self.tup = tup


a = A(namedtuple("tiger", "teeth smile tail"))
b = A(namedtuple("lion", "ears whiskers"))

m = a.tup("white", "wide")
n = b.tup("green", "wide")

print m.teeth
print n.ears

print dir(m)
print m.__dict__