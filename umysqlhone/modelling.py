__author__ = 'hone'

class Entity(object):

    def __init__(self, _dict = {}, **kwargs):
        if _dict != {} and  kwargs != {}:
            raise Exception("You should only include either named parameters or one dictionary")
        if _dict != {}:
            self._vars =_dict
        elif kwargs != {}:
            self._vars = kwargs


    def __getattr__(self, name):
        return self._vars.get( name, "")

    def __set__(self, instance, value):
        self._vars[instance] = value

    def fields(self):
        metac = self.Meta()
        d = dir(metac)
        d.reverse()
        metar = {}
        for i in d:
            if i == "__weakref__":
                break
            attr = getattr(metac, i, "")
            if isinstance(attr, Attribute):
                metar[i] = attr
        return metar

class Attribute(object):
    def __init__(self, **kwargs):
        self._vars = kwargs
    def vars(self):
        return self._vars

class MainMeta(object):
    pass

class Post(Entity):
    class Meta(MainMeta):
        id = Attribute(dog="Sausage")

class Tag(Entity):
    class Meta(MainMeta):
        tag = Attribute(dog="Poodle")

class Page(Post):
    class Meta(Post.Meta, Tag.Meta):
        name = Attribute(dog="German Shepard")
        slug = Attribute(dog="Beagle")

p1 = Post(name="Bingo")

print p1.name

p = Page({"name": "Bingo"})

print p.name

p.name = "Roger"

print p.name

print p.Meta.name.vars()
print p.Meta.id.vars()
print p.Meta.slug.vars()
print p.Meta.tag.vars()

print p.fields()

print p1.fields()

t = Tag(tag="bongo")

fields = t.fields()

for k, attr in fields.items():
    print k, attr.vars()