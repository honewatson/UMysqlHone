__author__ = 'hone'

from schematics.models import Model
from schematics.types import StringType, DateTimeType, IntType, URLType
from schematics.types.compound import ListType, ModelType

class Tag(Model):
    primary = "tag_id"
    table = "tag"
    tag_id = IntType()
    tag_name = StringType()
    slug = StringType()

class TagList(Model):
    tags = ListType(ModelType(Tag))

class InvertedIndex(Model):
    pass

class TagIndex(InvertedIndex):
    table = "tag_index"
    tag_id = IntType()
    product_id = IntType()


class Product(TagList):
    primary = "product_id"
    models = ['Product', 'TagList']
    product_id = IntType()
    name = StringType()

class SelectQuery(object):



    def __init__(self,
                 ob,
                 where_join,
                 table_number = 2,
                 where_set = False,
                 _set_where = False,
                 table_number_where="t1"):
        self.ob = ob()
        self.where_join = where_join
        self.table_number = table_number
        self.where_set = where_set
        self._set_where = _set_where
        self.table_number_where = table_number_where

    def _add_where_join(self, add):
        latest = self.where_join.pop()
        latest.append(add)
        self.where_join.append(latest)

    def Where(self, str):
        if not self.where_set:
            self.where_join.append([])
            self.where_set = True
            self._add_where_join(str)
        else:
            raise Exception("Where can only be set once")
        return self

    def And(self, str):
        if not len(self.where_join):
            raise Exception("You must set a Join or Where before using And!")
        self._add_where_join(str)
        return self

    def Join(self, str):
        self.where_join.append([])
        self._add_where_join(str())
        return self

    def _build_select(self):
        return "SELECT"

    def _build_fields(self):
        return " * "

    def _build_from(self):
        return "\nFROM %s" % self.ob.table

    def _reset_table_number(self):
        self.table_number = 2

    def _get_table_number(self):
        table_number = self.table_number
        self.table_number += 1
        ctable_number = "t%s" % str(table_number)
        return ctable_number

    def _build_join(self, join):
        table_number = self._get_table_number()

        ob = join.pop(0)

        if isinstance(ob, InvertedIndex):
            ob_primary = self.ob.primary
        else: ob_primary = ob.primary


        join_str = "\nJOIN %s as %s\n\tON %s.%s =  %s.%s" % (
            ob.table,
            table_number,
            self.table_number_where,
            self.ob.primary,
            table_number,
            ob_primary
        )

        ands = []

        if len(join):
            ands = ["\n\tAND %s.%s" % (table_number, _and) for _and in join]

        return "%s%s" % (join_str, "".join(ands))
        
    def _build_joins(self):

        if self.where_set:
            self._set_where = self.where_join.pop()


        if len(self.where_join):
            joins = [self._build_join(j) for j in self.where_join]
            return "\n%s" % "".join(joins)
        else: return ""

    def _build_and(self, where):
        _and = "%s.%s" % (self.table_number_where, where)
        return _and

    def _build_where(self):
        if not self.where_set:
            return ""
        else:
            wheres = [ self._build_and(where) for where in self._set_where]
        return "\nWHERE %s" % "\n\tAND ".join(wheres)

    def __str__(self):
        return "%s%s%s%s%s" % (
            self._build_select(),
            self._build_fields(),
            self._build_from(),
            self._build_joins(),
            self._build_where()
        )

def Query(ob):
    return SelectQuery(ob, [])

select = Query(Tag)
select.Join(TagIndex)
select.Join(TagIndex).And("tag_id = @tag_id")
select.Where("tag_id = @tag_id").And("tag_name = @tag_name")

select = Query(Tag).Join(TagIndex).Join(TagIndex).And("tag_id = @tag_id").Where("tag_id = @tag_id").And("tag_name = @tag_name")
print select.where_join
print select