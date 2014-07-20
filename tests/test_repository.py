from unittest import TestCase

__author__ = 'honhon'
import umysql
from umysqlhone.client import Factory, Query, Stm

class TestRepository(TestCase):

    def setUp(self):
        factory = Factory({ "db_host": "localhost", "db_port": 3306, "db_user": "root", "db_password": "", "db_database": "umysqlhone_test" })
        self.select = factory.select()

    def test_connect(self):
        self.select.connect()
        self.assertTrue(self.select._cnn.is_connected())

    def test_get_connection(self):
        self.assertIsInstance(self.select.get_connection(), umysql.Connection)

    def test_try_query(self):
        self.select.connect()
        try:
            result = self.select.try_query("SELECT 'Great Dane' as dog;").rows[0][0]
        except:
            self.fail()
        self.assertEqual(result, 'Great Dane')

    def test_close_connection(self):
        self.select.close_connection()
        self.assertFalse(self.select._cnn.is_connected())

    def test__query(self):
        try:
            result = self.select._query("SELECT 'Great Dane' as dog;", {}).rows[0][0]
        except:
            self.fail()
        self.assertEqual(result, 'Great Dane')

    def test__stm_builder(self):
        q = Query("q", "SELECT * FROM posts WHERE post_name = :post_name AND post_title = :post_title;")
        stm = self.select._stm_builder(q)
        self.assertIsInstance(stm, Stm)
        self.assertEqual(stm.execute, "EXECUTE q USING @post_name, @post_title;")
        self.assertEqual(stm.prepare, "PREPARE q FROM 'SELECT * FROM posts WHERE post_name = ? AND post_title = ?;';")
        self.assertEqual(stm.params, ['@post_name', '@post_title'])

    def test_prepare(self):
        q = Query("q", "SELECT * FROM posts WHERE post_name = :post_name AND post_title = :post_title;")
        self.select.connect()
        stm = self.select.prepare(q)
        self.assertIsInstance(stm, Stm)
        stm = self.select._stmcache.get(q.key, "")
        self.assertIsInstance(stm, Stm)

    def test_reconnect(self):
        self.test_prepare()
        self.select.close_connection()
        self.select.reconnect()
        keys = len(self.select._stmcache.keys())
        self.assertEqual(0, keys)
        self.assertTrue(self.select._cnn.is_connected())

    def test_set_params(self):
        self.select.connect()
        stm = Stm(["@dog"], "", "")
        self.select.set_params({"dog": "Border Collie"}, stm)
        result = self.select.query("SELECT @dog;")
        self.assertEqual(result[0]['@dog'], "Border Collie")


    def test_set_all_params(self):
        self.select.connect()
        params = {"ape": "Gorilla", "fish": "Tuna"}
        self.select.set_all_params(params)
        result = self.select.query("SELECT @ape, @fish;")
        self.assertEqual(result[0]['@ape'], "Gorilla")
        self.assertEqual(result[0]['@fish'], "Tuna")


