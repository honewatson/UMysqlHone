__author__ = 'honhon'
import re
from schematics.models import Model
from schematics.types import StringType, IntType, DateTimeType

class DateTimeModel(Model):
    published = DateTimeType()
    created_at = DateTimeType()
    updated_at = DateTimeType()

class Blog(Model):
    blog_id = IntType()
    primary = "blog_id"
    table = "blog"

class BlogDateTime(Blog, DateTimeModel):
    table = "blog_date_time"
    pass

class BlogTag(Blog):
    table = "blog_tag"
    tags = StringType()

b = BlogDateTime()

print b.to_primitive()
print b.primary

class Join(object):

    on = []
    def __init__(self, on):
        self.on.append(on)

    def And(self, on):

        self.on.append(on)
        return self


class Query(object):
    def _add_tnum(self, num):
        return "as %s" % num

class SelectQuery(Query):

    _from = None
    join = []

    def __init__(self, _from, factory):
        """

        @type _from: schematics.models.Model
        @type factory: Select
        @rtype:
        """
        self._from = _from
        self.factory = factory
        self.tnum = 1
        self.ctnum = "t1"

    def Join(self, on):
        j = self.factory.join(on)
        self.join.append(j)
        return j

    def build(self):
        return "%s%s%s%s" % (
            self.buildBegin(),
            self.buildFields(),
            self.buildFrom(),
            self.buildJoin(),
        )

    def buildBegin(self):
        return "SELECT "

    def buildFields(self):
        return "*\n"

    def _get_tnum(self):
        tnum = self.tnum
        self.tnum += 1
        self.ctnum = "t%s" % str(tnum)
        return self.ctnum

    def buildFrom(self):
        return "FROM %s %s" % (self._from.table, self._add_tnum(self._get_tnum()))

    def _buildJoin(self, j):
        return j.build(self.ctnum, self._from.primary, self._get_tnum())

    def buildJoin(self):
        joins = [self._buildJoin(j) for j in self.join]
        joins = "".join(joins)
        return joins



class JoinQuery(Query):

    def __init__(self, on, _and = []):
        self.on = on
        self._and = _and

    def And(self, arg):

        self._and.append(arg)
        print self._and
        return self

    def build(self, table, pkey, tnum):
        table_id = "%s.%s" % (table, pkey)
        first = self.on
        join = "\nJOIN %s %s \n\tON %s = %s.%s" % (first.table, self._add_tnum(tnum), table_id, tnum, first.primary)
        _and = ["\n\tAND %s.%s" % (tnum, i) for i in self._and]
        return "%s%s" % (join, "".join(_and))

class OrderQuery(object):
    pass


class Select(object):


    def __init__(self, select, join, order):
        self.select = select
        self.join = join
        self.order = order

    def __call__(self, name):
        return self.select(name, self)


select = Select(SelectQuery, JoinQuery, OrderQuery)

n = select(Blog())

n.Join(BlogDateTime()).And("published > @start_date")
n.Join(BlogDateTime()).And("published < @end_date")
n.Join(BlogTag()).And("tag = @tag")

print n.build()
#
# print n.join
# print n.join[0]._and
# print n.join[1]._and