__author__ = 'hone'

class PageModel(object):
    pass

class Attribute(object):
    pass

class IntAttr(Attribute):
    pass

class PrimaryAttr(IntAttr):
    pass

class TinyIntAttr(Attribute):
    pass

class SmallIntAttr(Attribute):
    pass

class PrimarySmallAttr(SmallIntAttr):
    pass


class StringAttr(Attribute):
    validator = ["monkey"]

class Model(object):
    pass

class InvertedIndex(Model):
    pass
