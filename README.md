UMysqlHone
==========

Python UMySql Utilities Which Include Generating Prepared Statements

Experimental only as a proof of concept.

```python

factory = Factory({ 
  "db_host": "localhost", 
  "db_port": 3306, 
  "db_user": "root", 
  "db_password": "", 
  "db_database": "umysqlhone_test"
})

select = factory.select()

posts = select.query("SELECT * FROM posts WHERE post_id = :post_id;", {"post_id": 1})

for post in posts:
  print(post.post_name)

```
