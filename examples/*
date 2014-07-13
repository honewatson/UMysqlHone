from umysqlhone.repository import Factory, Query

factory = Factory({ "db_host": "localhost", "db_port": 3306, "db_user": "root", "db_password": "", "db_database": "" })

select = factory.build("Select")

#q = Query("products", "SELECT * FROM catalog_product_entity WHERE entity_id > :entity_id LIMIT :limit;")

#results = db.query(q, {"entity_id": 5, "limit": 5})

cnn = select.get_connection()

q1 = Query("asl", "INSERT INTO asl (post_title, post_name) VALUES (:post_title, :post_name) ON DUPLICATE KEY UPDATE post_id = LAST_INSERT_ID(post_id), post_title = VALUES(post_title);")
q2 = Query("asls", "INSERT INTO asls (post_title, post_name) VALUES (:post_title, :post_name) ON DUPLICATE KEY UPDATE post_id = LAST_INSERT_ID(post_id), post_title = VALUES(post_title);")

insert = factory.insert()

# insert.connect()
# stm1 = insert.prepare(q1)
# stm2 = insert.prepare(q2)
# print stm1
# print stm1.prepare
# print stm1.execute
# print stm1.params
# sql = "SET :post_name = 'dblue'; SET :post_title = 'dBlue'; %s %s" % (stm1.execute, stm2.execute)
# cnn.query("SET :post_title = 'Blue';")
# cnn.query("SET :post_name = 'blue';")
#cnn.query(stm1.execute)
# cnn.query(stm2.execute)
params = {"post_name": "Blue", "post_title": "Red"}

results = insert.queries([q1, q2], params)

print results

print insert.query(q1, params)

params = {"post_name": "Bluea", "post_title": "Reda"}

print insert.query(q1, params)

params = {"post_name": "YBluea", "post_title": "YReda"}

print insert.query(q1, params)

#print results
from umysqlhone.repository import Row

from schematics.models import Model
from schematics.types import StringType, IntType, URLType

class Post(Model):
    post_id = IntType()
    post_title = StringType()
    post_name = StringType()
    image_link = URLType()
    post_excerpt = StringType()
    post_read_more = StringType()
    tag_names = StringType()

results = select.query("SELECT * FROM asl;", params, Post)

for row in results:
    print row.to_primitive()

results = select.query("SELECT * FROM asl where post_name = :post_name AND post_title = :post_title;", params)

for row in results:
    print row

results = select.query("SELECT * FROM asl where post_id = :post_id;", {"post_id": 2})

for row in results:
    print row

exe = factory.build('Execute')

print exe.query("UPDATE asl SET post_name = :post_name WHERE post_id = :post_id", {"post_id": 16, "post_name": "aparadise"})

print exe.query("CREATE TABLE IF NOT EXISTS asl1 LIKE asl;")

#print exe.query("")
#print exe.query("DELETE FROM asl where post_title LIKE :post_title", {"post_title": "%red%"})
#print exe.query("DELETE FROM asl where post_name = :post_name", params)

results = select.query("SELECT * FROM asl;", params, Post)

for row in results:
    print row.to_primitive()

# result = cnn.query("SELECT * FROM asl;", [])
#
# print result.rows

#
# for row in results:
#     for x,y in row:
#         print x,y
#
# class X(object):
#     bind_where = []
#     def bind(self, bind, params):
#         bind = "bind_%s" % bind
#         attr = getattr(self, bind)
#         for i in params:
#             attr.append(i)
#
#
# x = X()
#
# x.bind("where", ["a", "b"])
#
# class X(object):
#      def y(self, *args):
#         return args
#
# x = X()
#
#
# x.y(1, 2, 3)


# select = Select(Blog())
# select.join(BlogTag()).and("tag_id")
# select.join(BlogDateTime())
# select.limit(20)
# select.page(2)
# select.order(BlogDateTime().published, "DESC")