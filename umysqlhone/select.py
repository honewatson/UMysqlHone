class QueryInterface(object):
    def limit(self, limit): raise NotImplementedError()    
    def offset(self, offset): raise NotImplementedError()
    def __str__(self, offset): raise NotImplementedError()
    def get_quote_name_prefix(self): raise NotImplementedError()
    def get_quote_name_suffix(self): raise NotImplementedError()
    def bind_values(self): raise NotImplementedError()
    def bind_value(self): raise NotImplementedError()
    def get_bind_values(self): raise NotImplementedError()

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
    
    
    def __str__(self,):
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
        for k,v in bind_values.iter():
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

    
    def _set_flag(self, flag, enable = True):

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
        cond = self._quoter.quoteNamesIn(cond)
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
        self.order_by = [self._quoter.quoteNamesIn(col) for col in spec]   

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
    

