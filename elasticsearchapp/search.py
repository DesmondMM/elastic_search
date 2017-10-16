from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Search, Mapping, field as dsl_field
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

from . import models

connections.create_connection()

_m = Mapping('content')
_m.meta('dynamic_templates', [
    {
      "dates": {
            "path_match": "data.*_date",
            "mapping": {
              "type": "date"
            },
      }
    },
])


class BlogPostIndex(DocType):
    author = dsl_field.Text
    posted_date = dsl_field.Date
    title = dsl_field.Text
    text = dsl_field.Text

    class Meta:
        index = 'blogpost-index'


def bulk_indexing():
    BlogPostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.BlogPost.objects.all().iterator()))


def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response
