import re

class QueryInterface(object):
    def limit(self, limit): raise NotImplementedError()

    def offset(self, offset): raise NotImplementedError()

    def __str__(self, offset): raise NotImplementedError()

    def get_quote_name_prefix(self): raise NotImplementedError()

    def get_quote_name_suffix(self): raise NotImplementedError()

    def bind_values(self): raise NotImplementedError()

    def bind_value(self): raise NotImplementedError()

    def get_bind_values(self): raise NotImplementedError()


class SelectInterface(object):
    def set_paging(self, paging): raise NotImplementedError()

    def get_paging(self): raise NotImplementedError()

    def for_update(self, enable="1"): raise NotImplementedError()

    def distinct(self, enable="1"): raise NotImplementedError()

    def cols(self, cols): raise NotImplementedError()

    def froms(self, spec): raise NotImplementedError()

    def from_raw(self, spec): raise NotImplementedError()

    def from_sub_select(self, spec, name): raise NotImplementedError()

    def join(self, join, spec, cond=""): raise NotImplementedError()

    def inner_join(self, spec, cond=""): raise NotImplementedError()

    def left_join(self, spec, cond=""): raise NotImplementedError()

    def join_sub_select(self, join, spec, name, cond=""): raise NotImplementedError()

    def group_by(self, spec): raise NotImplementedError()

    def having(self, cond): raise NotImplementedError()

    def or_having(self, cond): raise NotImplementedError()

    def page(self, page): raise NotImplementedError()

    def union(self): raise NotImplementedError()

    def union_all(self): raise NotImplementedError()

    def where(self, cond): raise NotImplementedError()

    def or_where(self, cond): raise NotImplementedError()

    def order_by(self, spec): raise NotImplementedError()


class QueryBase(QueryInterface):
    
    bind_values = {}

    where = []

    bind_where = []

    order_by = []

    limit = 0

    offset = 0

    flags = []

    def __init__(self, _quoter):
        """
        @type _quoter: Quoter A helper for quoting identifier names.
        """
        self._quoter = _quoter


    def __str__(self, ):
        """
        Returns this query object as an sql string.
        """
        return self.build()


    def get_quote_name_prefix(self):
        """
        Returns the prefix to use when quoting identifier names
        """
        return self._quoter.get_quote_name_prefix()


    def get_quote_name_suffix(self):
        """
        Returns the suffix to use when quoting identifier names.
        """
        return self._quoter.get_quote_name_suffix()


    def _indent_csv(self, params):
        """
        Returns a list as an indented comma-separated values string.
        @type params: list
        @rtype string
        """
        return "\n    %s" % ",\n    ".join(params)

    def _indent(self, params):
        """
        Returns a list as an indented string.
        @type params: list
        @rtype string
        """
        return "\n    %s" % "\n    ".join(params)


    def bind_values(self, bind_values):
        """
        Binds multiple values to placeholders merges with existing values.
        @type bind_values: dict
        @rtype self
        """
        for k, v in bind_values.iter():
            self.bindValue(k, v)

        return self


    def bind_value(self, name, value):
        """
        Binds a single value to the query.
        @type name: string
        @type value: mixed
        """
        self.bind_values[name] = value
        return self


    def get_bind_values(self):
        """
        Gets the values to bind to placeholders.
        """
        return self.bind_values


    def _build_flags(self):
        """
        Builds the flags as a space-separated string.
        """
        if not self.flags:
            return ''# not applicable

        return "  %s" % " ".join(self.flag.keys())


    def _set_flag(self, flag, enable=True):

        """
        Sets or unsets specified flag.
        type flag: str
        type enable: bool
        rtype: None
        """
        if enable:
            self.flags[flag] = True
        else:
            del self.flags[flag]


    def _reset_flags(self):
        """
        Reset all query flags.
        """
        self.flags = {}


    def _add_where(self, andor, args):
        """
         
        Adds a WHERE condition to the query by AND or OR. If the condition has
        ?-placeholders, additional arguments to the method will be bound to
        those placeholders sequentially.
        
        @type andor: string Add the condition using this operator, typically
        'AND' or 'OR'.
        
        @type args: list Arguments for adding the condition.
        
        @rtype self
      
        """
        self._add_clause_cond_with_bind('where', andor, args)
        return self


    def _add_clause_cond_with_bind(self, clause, andor, args):


        """
        Adds conditions and binds values to a clause.
       
        @type clause: string The clause to work with, typically 'where' or
        'having'.
       
        @type andor: string  Add the condition using this operator, typically
        'AND' or 'OR'.
       
        @type args: list Arguments for adding the condition.
       
        @rtype None      
        """

        cond = args.pop()
        cond = self._quoter.quote_names_in(cond)
        # remaining args are bind values e.g., self.bind_where
        bind = "bind_%s" % clause
        attr = getattr(self, bind)
        for i in args:
            attr.append(i)

            # add condition to clause self.where
        clause = getattr(self, clause)
        if (len(clause)):
            clause.append("andor cond")
        else:
            clause.append(cond)


    def _build_where(self):
        """
        Builds the `WHERE` clause of the statement.
        @rtype: string
        """
        if not self.where:
            return '' # not applicable
        return " \nWHERE%s" % self._indent(self.where)


    def _add_order_by(self, spec):
        """
        Adds a column order to the query.
        @type spec: list
        """
        self.order_by = [self._quoter.quote_names_in(col) for col in spec]

        return self


    def _build_order_by(self):
        """
        Builds the `ORDER BY ...` clause of the statement.
        @rtype: str
        """

        if not self.order_by:
            return '' # not applicable

        return " \nORDER BY %s" % self._indent_csv(self.order_by)


    def _build_limit(self):
        """
        Builds the `LIMIT ... OFFSET` clause of the statement.
        @rtype: str
        """

        if self.limit:
            clause = "\nLIMIT %s" % self.limit
            if self.offset:
                clause = "%s OFFSET %s" % (clause, self.offset)

            return clause

        return '' # not applicable


class Select(SelectInterface, SelectInterface):
    
    union = []
    for_update = True
    cols = []
    _from = {}
    from_key = -1
    group_by = []
    having = []
    bind_having = []
    paging = 10

    def __str__(self):


        """


        Returns this object as an SQL statement string.

        @rtype:  string An SQL statement string.


        """

        union = ''
        if self.union:
            union = "%s\n" % "\n".join(self.union)

        return "%s%s" % (union, self.build())


    def set_paging(self, paging):


        """


        Sets the number of rows per page.

        @type paging: int The number of rows to page at.

        @rtype:  self


        """

        self.paging = int(paging)
        return self


    def get_paging(self):


        """


        Gets the number of rows per page.

        @rtype:  int The number of rows per page.


        """

        return self.paging


    def get_bind_values(self):


        """


        Gets the values to bind to placeholders.

        @rtype:  list|dict


        """

        bind_values = self.bind_values

        i = 1

        for value in self.bind_where:
            bind_values[i] = value
            i += 1

        for value in self.bind_having:
            bind_values[i] = value
            i += 1

        return bind_values


    def for_update(self, enable="1"):


        """


        Makes the select FOR UPDATE (or not).

        @type enable: bool Whether or not the SELECT is FOR UPDATE (default
        true).

        @rtype:  self


        """

        self.for_update = self._to_bool(enable)

    def _to_bool(self, enable):
        return bool(int( enable ) )
    
    def distinct(self, enable="1"):


        """


        Makes the select DISTINCT (or not).

        @type enable:bool Whether or not the SELECT is DISTINCT (default
        true).

        @rtype: self


        """

        self._set_flag('DISTINCT', enable)
        return self


    def cols(self, cols):


        """


        Adds columns to the query.

        Multiple calls to cols() will append to the list of columns, not
        overwrite the previous columns.

        @type cols: list|dict  The column(s) to add to the query. The elements can be
        any mix of these: `list|dict("col", "col AS alias", "col" => "alias")`

        @rtype:  self


        """
        for k,v in cols.iter():
            self._add_col(k, v)

        return self


    def _add_col(self, key, val):


        """


        Adds a column and alias to the columsn to be selected.

        @type key: mixed If an integer, ignored. Otherwise, the column to be
        added.

        @type val: mixed If key was an integer, the column to be added;
        otherwise, the column alias.


        """

        if isinstance( key, ( int, long ) ):
            self.cols.append(self.quoter.quote_names_in(val))
        else:
            self.cols.append(self.quoter.quote_names_in("%s AS %s" % (key, val)))
            


    def froms(self, spec):

        """
    
    
        Adds a FROM element to the query; quotes the table name automatically.
    
        @type spec: string The table specification; "foo" or "foo AS bar".
    
        @rtype:  self
    
    
        """
    
        return self.from_raw(self.quoter.quote_name(spec))


    def from_raw(self, spec):
        """
    
    
        Adds a raw unquoted FROM element to the query; useful for adding FROM
        elements that are functions.
    
        @type spec: string The table specification, e.g. "function_name()".
    
        @rtype:  self
    
    
        """
        self._from.append(spec)
        self.from_key += 1
    
    
    def from_sub_select(self, spec, name):
        """
    
    
        Adds an aliased sub-select to the query.
    
        @type spec: string|Select If a Select object, use as the sub-select;
        if a string, the sub-select string.
    
        @type name: string The alias name for the sub-select.
    
        @rtype: self
    
    
        """
    

        spec = re.sub("^", "\t\t", str(spec))
        self.append(
            """(\n\t\t%s\n\t\t\n) AS %s""" % (spec, self.quoter.quote_name(name))
        )
        self.from_key += 1
        return self
    
    
    def join(self, join, spec, cond=""):
        """
    
    
        Adds a JOIN table and columns to the query.
    
        @type join: string The join type: inner, left, natural, etc.
    
        @type spec: string The table specification; "foo" or "foo AS bar".
    
        @type cond: string Join on this condition.
    
        @rtype:  self
    
        @raises Exception
    
    
        """
    
        if not self._from:
            raise Exception("Cannot join() without froms() first.")
    
        join = "%s JOIN" % join
        join = join.lstrip().upper()
        spec = self.quoter.quote_name(spec)
        cond = self._fix_join_condition(cond)
        if not self._from.get(self.from_key):
            self._from[self.from_key] = []
        froms = "%s %s %s" % (join, spec, cond)
        self._from[self.from_key].append( froms.rsplit() )   
        return self
    
    
    def _fix_join_condition(self, cond):
        """
    
    
        Fixes a JOIN condition to quote names in the condition and prefix it
        with a condition type ('ON' is the default and 'USING' is recognized).
    
        @type cond: string Join on this condition.
    
        @rtype:  string
    
    
        """
    
        if not cond:
            return
    
        cond = self.quoter.quote_names_in(cond)
    

        if cond[:3].lsplit().upper() == "ON ":
            return cond
    
        if cond[:6].lsplit().upper() == "USING ":
            return cond
    
        return 'ON %s' % cond
    
    
    def inner_join(self, spec, cond=""):
        """
    
    
        Adds a INNER JOIN table and columns to the query.
    
        @type spec: string The table specification; "foo" or "foo AS bar".
    
        @type cond: string Join on this condition.
    
        @rtype: self
    
        @raises Exception
    
    
        """
    
        return self.join('INNER', spec, cond)
    
    
    def left_join(self, spec, cond=""):
        """
    
    
        Adds a LEFT JOIN table and columns to the query.
    
        @type spec: string The table specification; "foo" or "foo AS bar".
    
        @type cond: string Join on this condition.
    
        @rtype: self
    
        @raises Exception
    
    
        """
    
        return self.join('LEFT', spec, cond)
    
    
    def join_sub_select(self, join, spec, name, cond=""):
        """
    
    
        Adds a JOIN to an aliased subselect and columns to the query.
    
        @type join: string The join type: inner, left, natural, etc.
    
        @type spec: string|Select If a Select
        object, use as the sub-select; if a string, the sub-select
        command string.
    
        @type name: string The alias name for the sub-select.
    
        @type cond: string Join on this condition.
    
        @rtype: self
    
        @raises Exception
    
    
        """
    
        if not len(self._from.keys()):
            raise Exception('Cannot join() without from() first.')

        join = "%s JOIN" % join
        
        join = join.upper().lstrip()
        
        spec = "\n\t%s\n" % spec
        
        name = self.quoter.quote_name(name)
    
        cond = self._fix_join_condition(cond)
        
        if not len(self._from[self.from_key]):
            self._from[self.from_key] = []
            
        froms = "%s (%s) AS %s %s" % (join, spec, name, cond)
        
        self._from[self.from_key].append( froms )
        
        return self
    
    
    def group_by(self, spec):
        """
    
    
        Adds grouping to the query.
    
        @type spec: list|dict The column(s) to group by.
    
        @rtype: self
    
    
        """
    
        for col in spec:
            self.group_by.append(self.quoter.quote_names_in(col))
    
        return self
    
    
    def having(self, *args):
        """
    
    
        Adds a HAVING condition to the query by AND. If the condition has
        ?-placeholders, additional arguments to the method will be bound to
        those placeholders sequentially.
    
        @type cond: string The HAVING condition.
    
        @rtype: self
    
    
        """
    
        self._add_clause_cond_with_bind('having', 'AND', args)
        return self
    
    
    def or_having(self, *args):
        """
    
    
        Adds a HAVING condition to the query by AND. If the condition has
        ?-placeholders, additional arguments to the method will be bound to
        those placeholders sequentially.
    
        @type cond: string The HAVING condition.
    
        @rtype: self
    
        @see having()
    
    
        """
    
        self._add_clause_cond_with_bind('having', 'OR', args)
        return self
    
    
    def page(self, page):
        """
    
    
        Sets the limit and count by page number.
    
        @type page: int Limit results to this page number.
    
        @rtype: self
    
    
        """
    
        # reset the count and offset
        self.limit = 0
        self.offset = 0
    
        # determine the count and offset from the page number
        page = int(page)
        if page > 0:
            self.limit = self.paging
            self.offset = self.paging * (page - 1)
    
    
        # done
        return self
    
    
    def union(self):
        """
    
    
        Takes the current select properties and retains them, then sets
        UNION for the next set of properties.
    
        @rtype:  self
    
    
        """
    
        self.union.append("%s\nUNION" % self.build())
        self.reset()
        return self
    
    
    def union_all(self):
        """
    
    
        Takes the current select properties and retains them, then sets
        UNION ALL for the next set of properties.
    
        @rtype:  self
    
    
        """
    
        self.union.append("%s\nUNION ALL" % self.build())
        self.reset()
        return self
    
    
    def _reset(self):
        """
    
    
        Clears the current select properties; generally used after adding a
        union.
    
        @rtype:  null
    
    
        """
    
        self.resetFlags()
        self.cols = []
        self._from      = {}
        self.from_key = -1
        self.where = []
        self.group_by = []
        self.having = []
        self.order_by = []
        self.limit = 0
        self.offset = 0
        self.for_update = False
    
    
    def _build(self):
        """
    
    
        Builds this query object into a string.
    
        @rtype:  string
    
    
        """
    
        return 'SELECT %s%s%s%s%s%s%s%s%s' % (
            self._build_flags(),
            self._build_cols(),
            self._build_from(), # includes JOIN
            self._build_where(),
            self._build_group_by(),
            self._build_having(),
            self._build_order_by(),
            self._build_limit(),
            self._build_for_update(),           
        )

    
    
    def _build_cols(self):
        """
    
    
        Builds the columns clause.
    
        @rtype:  string
    
        @raises Exception when there are no columns in the SELECT.
    
    
        """
    
        if not self.cols:
            raise Exception('No columns in the SELECT.')
    
        return self._indent_csv(self.cols)
    
    
    def _build_from(self):
        """
    
    
        Builds the FROM clause.
    
        @rtype:  string
    
    
        """
    
        if not len(self._from.keys()):
            return '' # not applicable
    
        refs = ["\n".join(f) for f in self.froms]
    
        return '%sFROM' % self._indent_csv(refs)
    
    
    def _build_group_by(self):
        """
    
    
        Builds the GROUP BY clause.
    
        @rtype:  string
    
    
        """
    
        if not len(self.group_by):
            return '' # not applicable
    
        return '\nGROUP BY%s' % self._indent_csv(self.group_by)
    
    
    def _build_having(self):
        """
    
    
        Builds the HAVING clause.
    
        @rtype:  string
    
    
        """
    
        if not len(self.having):
            return '' # not applicable
    
        return '\n%sHAVING' % self.indent(self.having)
    
    
    def _build_for_update(self):
        """
    
    
        Builds the FOR UPDATE clause.
    
        @rtype:  string
    
    
        """
    
        if not self.for_update:
            return '' # not applicable
    
        return '\nFOR UPDATE'
    
    
    def where(self, *args):
        """
    
    
        Adds a WHERE condition to the query by AND. If the condition has
        ?-placeholders, additional arguments to the method will be bound to
        those placeholders sequentially.
    
        @type *args: string The WHERE condition. ...bind arguments to bind to placeholders
    
        @rtype:  self
    
    
        """
    
        self._add_where('AND', args)
        return self
    
    
    def or_where(self, *args):
        """
    
    
        Adds a WHERE condition to the query by OR. If the condition has
        ?-placeholders, additional arguments to the method will be bound to
        those placeholders sequentially.
    
        @type *args: string The WHERE condition. ...bind arguments to bind to placeholders

    
        @rtype:  self
    
        @see where()
    
    
        """
    
        self._add_where('OR', args)
        return self
    
    
    def limit(self, limit):
        """
    
    
        Sets a limit count on the query.
    
        @type limit: int The number of rows to select.
    
        @rtype:  self
    
    
        """
    
        self.limit = int(limit)
        return self
    
    
    def offset(self, offset):
        """
    
    
        Sets a limit offset on the query.
    
        @type offset: int Start returning after this many rows.
    
        @rtype:  self
    
    
        """
    
        self.offset = int(offset)
        return self
    
    
    def order_by(self, spec):
        """
    
    
        Adds a column order to the query.
    
        @type spec: list|dict The columns and direction to order by.
    
        @rtype:  self
    
    
        """
    
        return self._add_order_by(spec)