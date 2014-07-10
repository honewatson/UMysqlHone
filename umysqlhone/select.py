__author__ = 'honhon'

class Query(object):

    def __init__(self):
        self._groupby = []


    def _add_tnum(self, num):
        return "as %s" % num


    def GroupBy(self, _type):
        self._groupby.append(_type)
        return self

    def _collect_groupbys(self):
        l =  [ "%s.%s" % (self.ctnum, gb) for gb in self._groupby ]
        if not len(l):
            l = []
        return l


class SelectQuery(Query):

    _from = None
    join = []

    def __init__(self, _from, factory,  **kwargs):
        """

        @type _from: schematics.models.Model
        @type factory: Select
        @rtype:
        """
        self._from = _from
        self.factory = factory
        self.tnum = 1


        super(SelectQuery, self).__init__(**kwargs)


    def Join(self, on, join="JOIN"):
        j = self.factory.join(on, join)
        self.join.append(j)
        return j

    def LeftJoin(self, on):
        return self.Join(on, "LEFT JOIN")

    def RightJoin(self, on):
        return self.Join(on, "RIGHT JOIN")

    def InnerJoin(self, on):
        return self.Join(on, "INNER JOIN")

    def build(self):
        return "%s%s%s%s%s" % (
            self.buildBegin(),
            self.buildFields(),
            self.buildFrom(),
            self.buildJoin(),
            self.buildGroupBys()
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

    def buildGroupBys(self):

        l = self._collect_groupbys()
        for j in self.join:
            l.extend(j._collect_groupbys())

        if len(l):
            return "\nGROUP BY %s" % ", ".join(l)
        else: return ""

class JoinQuery(Query):


    def __init__(self, on, join, **kwargs):
        self.on = on
        self._and = []
        self.join = join

        super(JoinQuery, self).__init__(**kwargs)

    def And(self, arg):

        self._and.append(arg)

        return self

    def build(self, table, pkey, tnum):
        self.ctnum = tnum
        table_id = "%s.%s" % (table, pkey)
        first = self.on
        join = "\n%s %s %s \n\tON %s = %s.%s" % (self.join, first.table, self._add_tnum(tnum), table_id, tnum, first.primary)
        _and = ["\n\tAND %s.%s" % (tnum, i) for i in self._and]
        return "%s%s" % (join, "".join(_and))



class OrderQuery(object):
    pass


class _Select(object):


    def __init__(self, select, join):
        self.select = select
        self.join = join


    def __call__(self, name):
        return self.select(name, self)

Select = _Select(SelectQuery, JoinQuery)