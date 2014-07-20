__author__ = 'honhon'
from umysqlhone.client import Query, Factory, Stm

factory = Factory({ "db_host": "localhost", "db_port": 3306, "db_user": "root", "db_password": "", "db_database": "umysqlhone_test" })
select = factory.select()


# q = Query("q", "SELECT * FROM asl WHERE post_name = :post_name AND post_title = :post_title;")
# stm = select._stm_builder(q)
# print stm.execute
# print stm.prepare
# print stm.params
#
# cnn = select.get_connection()
#
# stm = Stm(["@dog"], "", "")
#
# select.set_params({"dog": "Border Collie"}, stm)
#
# print select.query("SELECT @dog;")
#
# print select._query("SELECT 'Great Dane' as dog;", {}).rows[0][0]

