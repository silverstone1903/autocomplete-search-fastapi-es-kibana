from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import RequestError
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

index_name = "movies"

es = Elasticsearch(hosts=[{"scheme": "http", "host": "host.docker.internal", "port": 9200}], max_retries=30,
                   retry_on_timeout=True, request_timeout=30)

if not es.ping():
    raise ValueError("Connection failed.")
else:
    print("Successfully connected to Elasticsearch.")

movies = pd.read_feather("/app/data/movies.feather")

index = {
    "settings": {
        "analysis": {
            "filter": {
                "my_ascii_folding": {
                    "type": "asciifolding",
                    "preserve_original": "true"
                },
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 10
                },
                "turkish_lowercase": {
                    "type":       "lowercase",
                    "language":   "turkish"
                },
                "turkish_stemmer": {
                    "type":       "stemmer",
                    "language":   "turkish"}
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "turkish_lowercase",
                        "turkish_stemmer",
                        "autocomplete_filter",
                        "my_ascii_folding"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "movies": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "standard"
            }
        }
    }
}


def dataframe_to_es(df, es_index):
    for df_idx, line in df.iteritems():
        yield {
            "_index": es_index,
            "_id": df_idx,
            "type": "_doc",
            "_source": {
                "movies": line

            }
        }


try:
    es.indices.delete(index_name)
except:
    print("There is no index called %s." % index_name)
    print("Creating index %s." % index_name)
    es.indices.create(index=index_name, ignore=400, body=index)

helpers.bulk(es, dataframe_to_es(
    movies["movie_name"], index_name), raise_on_error=False)

print("Indexing complete & Indexed %s rows." % movies.shape[0])
