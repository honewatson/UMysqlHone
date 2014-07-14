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

    def _check_iter(self, value, attr):
        if isinstance(value, list):
            return [m.to_primitive() for m in value]
        elif isinstance(value, dict):
            return {k: v.to_primitive() for k, v in value.items()}
        elif isinstance(value, Entity):
            return value.to_primitive()
        else: return value

    def _get_var(self, k, v):
        if getattr(self, k, ""): return self._check_iter(getattr(self, k, ""), v)
        elif self._vars.get(k, ""): return self._check_iter(self._vars.get(k, "") ,v)
        elif getattr(v, "default", ""): return getattr(v, "default", "")
        else: return None


    def to_primitive(self):
        fields  = self.fields()
        return {
            k: self._get_var(k, v)
            for k, v in fields.items()
        }

class Attribute(object):
    def __init__(self, **kwargs):

        self._vars = kwargs

    def set(self, k, v):
        self._vars[k] = v

    def vars(self):
        return self._vars

    def get_var(self, k):
        return self._vars.get(k)

class MainMeta(object):
    pass

IdType = Attribute(dog="Sausage")
NameType = Attribute(dog="German Shepard")

SlugType = Attribute(dog="Beagle")

class Post(Entity):
    class Meta(MainMeta):
        post_id = IdType

class Tag(Entity):
    class Meta(MainMeta):
        tag_id = IdType
        name = NameType
        slug = SlugType

class Tags(Entity):
    class Meta(MainMeta):
        tags = Attribute(dog="Toy Poodle", model=Tag, default=[])

class Page(Post):
    class Meta(Post.Meta, Tags.Meta):
        name = NameType
        slug = SlugType

p1 = Post(name="Bingo")

print p1.name

p = Page({"name": "Bingo"})
p.tags = [Tag(name="Tiger")]
print p.to_primitive()
p = Page({"name": "Bongo"})
print p.to_primitive()
print p.name

p.name = "Roger"

print p.name
print p._vars

print p.name

print p.Meta.name.vars()
print p.Meta.post_id.vars()
print p.Meta.slug.vars()
print p.Meta.name.vars()

print p.Meta.tags.vars()

print p.fields()

print p1.fields()

t = Tag(tag="bongo")

fields = t.fields()

for k, attr in fields.items():
    print k, attr.vars()

tags = Tags(tags=[Tag(name="Tag One"), Tag(name="Tag Two")])



print tags.to_primitive()

print p.to_primitive()
#
# tags.tags = [Tag(name="Bongo"), Tag(name="Bingo")]
#
# print tags.to_primitive()