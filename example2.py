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




class SelectQuery(object):

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

    def buildFrom(self):
        return "FROM %s\n" % self._from.table

    def buildJoin(self):
        joins = [j.build(self._from.table, self._from.primary) for j in self.join]
        joins = "\n%s".join(joins)
        return joins



class JoinQuery(object):

    _and = []
    def __init__(self, on):
        self.on = on

    def And(self, arg):
        self._and.append(arg)
        return self

    def build(self, table, pkey):
        table_id = "%s.%s" % (table, pkey)
        first = self.on
        join = "\nJOIN %s\nON %s = %s.%s" % (first.table, table_id, first.table, first.primary)
        _and = ["\nAND %s" % i for i in self._and]
        return "%s%s" % (join, "".join(_and))

class OrderQuery(object):
    pass


class Select(object):


    def __init__(self, select, join, order):
        self.select = select
        self.join = join
        self.order = order

    def __call__(self, name):
        return self.select(name, Select(self.select, self.join, self.order))


select = Select(SelectQuery, JoinQuery, OrderQuery)

n = select(Blog())

n.Join(BlogDateTime()).And("published > @start_date").And("published < @end_date")

print n.build()

