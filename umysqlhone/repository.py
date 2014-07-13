import itertools
import umysql
import re

class Query(object):
    def __init__(self, key, sql):
        self.key = key
        self.sql = sql

class Qfactory(object):
    def get(self, sql):
        return Query("A%s" % str(sql.__hash__()).strip("-"), sql)

class StmCache(dict):
    pass

class Stm(object):
    def __init__(self, params, execute, prepare):
        """
        :param params: dict
        :param execute: str MySQL execute
        :param prepare: str MySQL prepare
        :return:
        """
        self.params = params
        self.execute = execute
        self.prepare = prepare

class Repository(object):

    def __init__(self, _cnn, _config, _stmcache, _match, qfactory):
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
        self.qfactory = qfactory

    def _stm_builder(self, query):
        """
        Factory to build statement
        @type query: Query
        @rtype = Stm
        """
        tokens = self._match.findall(query.sql)
        if len(tokens):
            _execute = "EXECUTE %s USING %s;" % (query.key, ", ".join(tokens))
        else:
            _execute = "EXECUTE %s;" % (query.key)
        return Stm(
            tokens,
            _execute,
            "PREPARE %s FROM '%s';" % (query.key, self._match.sub("?", query.sql))
        )

    def prepare(self, query):
        """
        Creates and caches a prepared statement then executes and returns Stm
        @type: Query
        @rtype: Stm
        """
        if isinstance(query, basestring):
            query = self.qfactory.get(query)
        if not self._stmcache.get(query.key, ""):
            self._stmcache[query.key] = stm = self._stm_builder(query)
            self.try_query(stm.prepare)
        return self._stmcache.get(query.key)

    def reconnect(self):
        """
        Reconnects to MySql
        :return:
        """
        self._cnn.connect(
            self._config['db_host'],
            self._config['db_port'],
            self._config['db_user'],
            self._config['db_password'],
            self._config['db_database']
        )
        self._stmcache.clear()

    def connect(self):
        """
        Ensures there is a connection to MySql
        :return:
        """
        if not self._cnn.is_connected():
            self.reconnect()

    def get_connection(self):
        """
        Returns a ultramysql connection
        @rtype:
        """
        self.connect()
        return self._cnn

    def close_connection(self):
        """
        Closes MySQL connection
        :return:
        """
        self._cnn.close()

    def set_params(self, params, stm):
        """
        @type params: dict
        @type stm: Stm
        @rtype:
        """
        for param in stm.params:
            _set = "SET %s = %s" % (param, "%s")
            self._cnn.query(_set, [params[param.lstrip("@")]])

    def set_all_params(self, params):
        """
        @type params: dict
        @rtype:
        """
        for param, value  in params.items():
            _set = "SET @%s = %s" % (param, "%s")
            self._cnn.query(_set, [value])

    def try_query(self, _execute, _params = []):
        """
        @type _execute: str
        @type _params: list
        @rtype: mixed
        """
        return self._cnn.query(_execute, _params)

    def _query(self, query, params):
        """
        @type query: Query
        @type params: dict
        @rtype: list
        """
        self.connect()
        stm = self.prepare(query)
        self.set_params(params, stm)
        return self.try_query(stm.execute)

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
        @type params: dict
        @type _type: Row
        @rtype: list
        query = {
            'sql': 'SELECT entity_id, sku FROM catalog_product_entity WHERE entity_id > %s LIMIT 10',
            'params': ('entity_id')
        }
        params = ["entity_id": 5, "sku": "biggie"]
        """

        results = self._query(query, params)
        column_names = [r[0] for r in results.fields]
        if _type:
            return [_type(dict(itertools.izip(column_names, row))) for row in results.rows]
        else:
            return [Row(itertools.izip(column_names, row)) for row in results.rows]

class Insert(Repository):

    def get_last_insert_id(self):
        last_row_id = self._cnn.query('SELECT LAST_INSERT_ID();')
        return last_row_id.rows[0][0]

    def query(self, query, params={}):

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

        self._query(query, params)
        return self.get_last_insert_id()


    def _helper_multi_query(self, query):
        """
        @type query: string
        @rtype: int
        """
        stm = self.prepare(query)
        self.try_query(stm.execute)
        return self.get_last_insert_id()


    def queries(self, queries, params={}):
        """
        Used for same params but multiple tables
        @type queries: list
        @type params: dict
        @rtype: list
        """
        self.connect()
        self.set_all_params(params)
        query_key_results = { query.key: self._helper_multi_query(query) for query in queries}
        return query_key_results

class Execute(Repository):
    def query(self, query, params={}):
        """
        @type query: Query|str
        @rtype params: dict
        @rtype int
        """
        result = self._query(query, params)
        return result[0]


class Factory(object):

    connection = None

    cls = {
        "Select": Select,
        "Insert": Insert,
        "Execute": Execute
    }

    compile = re.compile("@[a-zA-Z0-9_]+")

    def __init__(self, config):
        """
        @type config: dict
        """
        self.config = config

    def build(self, cls):
        """
        @type cls: str
        @rtype: Repository
        """
        if not self.connection:
            self.connection = umysql.Connection()
        cls = self.cls.get(cls)
        return cls(umysql.Connection(), self.config, StmCache({}), self.compile, Qfactory())

    def select(self):
        """
        @rtype: Select
        """
        return self.build("Select")

    def insert(self):
        """
        @rtype: Insert
        """
        return self.build("Insert")

    def execute(self):
        """
        @rtype: Insert
        """
        return self.build("Execute")
