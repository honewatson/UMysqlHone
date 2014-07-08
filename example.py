
from umysqlhone.Repository import Factory, Query

factory = Factory({ "db_host": "localhost", "db_port": 3306, "db_user": "root", "db_password": "", "db_database": "" })

db = factory.build("Select")

q = Query("products", "SELECT * FROM catalog_product_entity WHERE entity_id > @entity_id LIMIT @limit;")

results = db.query(q, {"entity_id": 5, "limit": 5})

for row in results:
    for x,y in row:
        print x,y

