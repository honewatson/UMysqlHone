__author__ = 'hone'

class Entity(object):

    def __init__(self, _dict = {}, **kwargs):
        if _dict != {} and  kwargs != {}:
            raise Exception("You should only include either named parameters or one dictionary")
        if _dict != {}:
            self._vars =_dict
        elif kwargs != {}:
            self._vars = kwargs
        self.set_defaults()

    def __getattr__(self, name):
        return self._vars.get( name, "")

    def __set__(self, instance, value):
        self._vars[instance] = value

    def fields(self):
        if not getattr(self, "_fields"):
            self._attrs = self.Attrs()
            d = dir(self._attrs)
            d.reverse()
            Attrsr = {}
            for i in d:
                if i == "__weakref__":
                    break
                attr = getattr(self._attrs, i, "")
                if isinstance(attr, Attribute):
                    Attrsr[i] = attr
            self._fields = Attrsr
        return self._fields

    def set_defaults(self):
        self._vars = self.to_primitive()

    def _check_primitive(self, v):
        if getattr(v, 'to_primitive', ""): return v.to_primitive()
        else: return v

    def _check_iter(self, value, attr):
        if isinstance(value, list):
            return [self._check_primitive(m) for m in value]
        elif isinstance(value, dict):
            return {k: self._check_primitive(v) for k, v in value.items()  }
        elif isinstance(value, Entity):
            return value.to_primitive()
        else: return value

    def _get_var(self, k, v):
        if getattr(self, k, ""): return self._check_iter(getattr(self, k, ""), v)
        elif self._vars.get(k, ""): return self._check_iter(self._vars.get(k, "") ,v)
        elif isinstance(v, Attribute): return v.get_var("default")
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


IdType = Attribute(dog="Sausage")

NameType = Attribute(dog="German Shepard")

SlugType = Attribute(dog="Beagle")


class Attrs(object):
    pass

class Post(Entity):
    class Attrs(Attrs):
        post_id = IdType

class Tag(Entity):
    class Attrs(Attrs):
        tag_id = IdType
        name = NameType
        slug = SlugType

TagsType = Attribute(dog="Toy Poodle", model=Tag, default=[])

class Tags(Entity):
    class Attrs(Attrs):
        tags = TagsType

class Page(Post):
    class Attrs(Post.Attrs, Tags.Attrs):
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

print p.Attrs.name.vars()
print p.Attrs.post_id.vars()
print p.Attrs.slug.vars()
print p.Attrs.name.vars()

print p.Attrs.tags.vars()

print p.fields()

print p1.fields()

t = Tag(tag="bongo")

fields = t.fields()

for k, attr in fields.items():
    print k, attr.vars()

tags = Tags(tags=[Tag(name="Tag One"), Tag(name="Tag Two")])



print tags.to_primitive()

print p.to_primitive()

p = Page({"name": "Tongo"})

p.tags.append(Tag(name="Monkey"))


#
# tags.tags = [Tag(name="Bongo"), Tag(name="Bingo")]
#
print p.to_primitive()