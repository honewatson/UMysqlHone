__author__ = 'honhon'
import re
from schematics.models import Model
from schematics.types import StringType, IntType, DateTimeType

class DateTimeModel(Model):
    published = DateTimeType()
    created_at = DateTimeType()
    updated_at = DateTimeType()

class Blog(Model):
    blog_id = IntType()
    name = StringType()
    author = IntType()
    primary = "blog_id"
    table = "blog"

class BlogDateTime(Blog, DateTimeModel):
    table = "blog_date_time"
    pass

class BlogTag(Blog):
    table = "blog_tag"
    tags = StringType()

b = BlogDateTime()



print b.to_primitive()
print b.primary

class Join(object):

    on = []
    def __init__(self, on):
        self.on.append(on)

    def And(self, on):

        self.on.append(on)
        return self








from umysqlhone.select import  Select

select = Select(Blog()).GroupBy("name")

select.Join(BlogDateTime()).And("published > @start_date")
select.Join(BlogDateTime()).And("published < @end_date")
select.LeftJoin(BlogTag()).And("tag = @tag").GroupBy("tag")

print select.join[0].on.table
print select.join[1].on.table
print select.join[2].on.table
print select.build()

print b.blog_id
#
# print n.join
# print n.join[0]._and
# print n.join[1]._and

