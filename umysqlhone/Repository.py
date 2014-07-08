import itertools
import umysql
import re

class Query(object):

    def __init__(self, key, sql):
        self.key = key
        self.sql = sql

class StmCache(dict):
    pass

class Stm(object):

    def __init__(self, params, execute, prepare):
        self.params = params
        self.execute = execute
        self.prepare = prepare

class Repository(object):

    def __init__(self, _cnn, _config, _stmcache, _match):
        """
        @type _cnn:
        @type _config: dict
        @type _stmcache: Stmcache
        @type _match: re.compile("@[a-zA-Z0-9]+")
        cnn = umysql.Connection()
        cnn.connect('127.0.0.1', 3306, 'root', 'password', 'dbname')
        """
        self._cnn = _cnn
        self._config = _config
        self._stmcache = _stmcache
        self._match = _match

    def _stm_builder(self, query):
        tokens = self._match.findall(query.sql)
        return Stm(
            tokens,
            "EXECUTE %s USING %s;" % (query.key, ", ".join(tokens)),
            "PREPARE %s FROM '%s';" % (query.key, self._match.sub("?", query.sql))
        )

    def _prepare(self, query):
        if not self._stmcache.get(query.key, ""):
            self._stmcache[query.key] = stm = self._stm_builder(query)
            self._cnn.query(stm.prepare)
            #"PREPARE stmt1 FROM 'SELECT * FROM catalog_product_entity WHERE entity_id = ? LIMIT 5'"
        return self._stmcache.get(query.key)

    def reconnect(self):
        self._cnn.connect(
            self._config['db_host'],
            self._config['db_port'],
            self._config['db_user'],
            self._config['db_password'],
            self._config['db_database']
        )
        self._stmcache.clear()

    def connect(self):
        if not self._cnn.is_connected():
            self.reconnect()

    def _query(self, query, params, _type = None):
        """
        @type query: Query
        @type params: dict
        @rtype: list
        """
        self.connect()

        # try:

        stm = self._prepare(query)

        for param in stm.params:
            _set = "SET %s = %s" % (param, "%s")
            self._cnn.query(_set, [params[param.lstrip("@")]])

        return self._cnn.query(stm.execute)


        # except Exception as e:
        #     #print e
        #     return False


    def query(self, query, params, _type = None): raise NotImplementedError()

class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

class Select(Repository):

    def query(self, query, params={}, _type = None):

        """
        @type query: dict
        @type params: tict
        @rtype: list
        query = {
            'sql': 'SELECT entity_id, sku FROM catalog_product_entity WHERE entity_id > %s LIMIT 10',
            'params': ('entity_id')
        }
        params = ["entity_id": 5, "sku": "biggie"]
        """

        # try:
        results = self._query(query, params)
        column_names = [r[0] for r in results.fields]
        if _type:
            return [_type(itertools.izip(column_names, row)) for row in results.rows]
        else:
            return [itertools.izip(column_names, row) for row in results.rows]
        #
        # except Exception, e:
        #     return "Some Exception"

class Insert(Repository):

    def query(self, query, params={}, _type = None):

        """
        @type query: dict
        @type params: tict
        @rtype: list
        query = {
            'sql': 'SELECT entity_id, sku FROM catalog_product_entity WHERE entity_id > %s LIMIT 10',
            'params': ('entity_id')
        }
        params = ["entity_id": 5, "sku": "biggie"]
        """

        # try:
        self._query(query, params)
        last_row_id = self._cnn.query('SELECT LAST_INSERT_ID();')
        return last_row_id.rows[0][0]

class Factory(object):

    connection = None

    cls = {
        "Select": Select
    }

    compile = re.compile("@[a-zA-Z0-9_]+")

    def __init__(self, config):
        self.config = config

    def build(self, cls):
        if not self.connection:
            self.connection = umysql.Connection()
        cls = self.cls.get(cls)
        return cls(umysql.Connection(), self.config, StmCache({}), self.compile)


