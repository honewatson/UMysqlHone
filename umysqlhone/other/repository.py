
class Query(object):

    _select = "SELECT {fields} \nFROM {main} {joins} {where} {groupby} {having} {orderby} {limit}"
    _join =  "\n{join type} JOIN {join} \nON main.{main_primary} = {join_alias}.{join_primary}"
    _and = "\n\tAND {table}.{field} = :{table}{field}"

    def __init__(self, main, **kwargs):
        self._main = main
        self.kwargs = kwargs

    def reset(self):
        self._fields = "*"
        self._joins = ""
        self._groupby = ""
        self._having = ""
        self._orderby = ""
        self._limit = ""

    def fields(self):
        return "*"

    def main(self):
        return type(self._main).__name__

    def joins(self):
        return ""

    def where(self):
        return ""

    def groupby(self):
        return ""

    def having(self):
        return ""

    def orderby(self):
        return ""

    def limit(self):
        return ""

    def __str__(self):
        return self.__class__._select.format(
            fields = self.fields(),
            main = self.main(),
            joins = self.joins(),
            where = self.where(),
            groupby = self.groupby(),
            having = self.having(),
            orderby = self.orderby(),
            limit = self.limit()
        )


#from otbmodels import BlogModel

#print Query(BlogModel())

def test(what):
    print what

