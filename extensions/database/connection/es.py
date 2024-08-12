from elasticsearch import AsyncElasticsearch, Elasticsearch
import os

ELASTIC_SEARCH_HOST = os.environ.get("ELASTIC_SEARCH_HOST", "localhost")
ELASTIC_SEARCH_PORT = os.environ.get("ELASTIC_SEARCH_PORT", "9200")
URLS = ["http://{ELASTIC_SEARCH_HOST}:{ELASTIC_SEARCH_PORT}"]


# Function to get Elasticsearch connection
def get_connection():
    return Elasticsearch(URLS)


def get_async_connection():
    return AsyncElasticsearch(URLS)


# Dependency with cleanup
def es_dependency():
    es = get_connection()
    try:
        yield es
    finally:
        # Cleanup code goes here (if necessary)
        # Example: es.close() if the client requires explicit closing
        pass
