__author__ = 'honhon'
from umysqlhone.client import Query, Factory, Stm, Row
from wheezy.core.benchmark import Benchmark
import itertools
factory = Factory({ "db_host": "localhost", "db_port": 3306, "db_user": "root", "db_password": "", "db_database": "test" })
select = factory.select()

q = Query("q", "SELECT * FROM api_small_links WHERE post_id = :post_id;")

# print select.query(q, {"post_id": 1})

cnn = select.get_connection()

def q1():
    result = select.query(q, {"post_id": 1})

def q2(_type=None):
    results = cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
    column_names = [r[0] for r in results.fields]
    if _type:
        result = [_type(dict(itertools.izip(column_names, row))) for row in results.rows]
    else:
        result = [Row(itertools.izip(column_names, row)) for row in results.rows]

def q3(_type=None):
    results = cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
    column_names = [r[0] for r in results.fields]
    result = [Row(itertools.izip(column_names, row)) for row in results.rows]

def q4(_type=None):
    results = cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
    column_names = [r[0] for r in results.fields]
    result = []
    for row in results.rows:
        result.append(Row(itertools.izip(column_names, row)))

from collections import namedtuple

column_names = []

class XY(object):
    def __init__(self, cnn, column_names=None, nm=None):
        self.cnn = cnn
        if column_names is None:
            self.column_names = []
        self.nm = nm

    def q5(self, _type=None):
        results = self.cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
        if not self.column_names:
            self.column_names = [r[0] for r in results.fields]
        result = [Row(itertools.izip(self.column_names, row)) for row in results.rows]

    def q6(self, _type=None):
        results = self.cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
        if not self.column_names:
            self.column_names = [r[0] for r in results.fields]
        result = [dict(itertools.izip(self.column_names, row)) for row in results.rows]

    def q7(self, _type=None):
        results = self.cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
        if not self.column_names:
            self.column_names = [r[0] for r in results.fields]
        result = [{v:row[index] for index, v in enumerate(self.column_names)} for row in results.rows]

    def q8(self, _type=None):
        results = self.cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
        if not self.nm:
            self.nm = namedtuple("nm", " ".join([r[0] for r in results.fields]))
        result = [self.nm(*row) for row in results.rows]

    def q9(self, _type=None):
        results = self.cnn.query("SELECT * FROM api_small_links WHERE post_id = %s", (1,))
        nm = namedtuple("nm", " ".join([r[0] for r in results.fields]))
        result = [nm(*row) for row in results.rows]

xy = XY(select.get_connection())
#print q2()
xy.q7()
xy.q5()


p = Benchmark((
    q1,
    q2,
    q3,
    q4,
    xy.q5,
    xy.q6,
    xy.q7,
    xy.q8,
    #xy.q9
), 10000)

p.report('public')