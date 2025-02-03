from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

class ElasticsearchService:
    """
    Handles Elasticsearch operations: caching transactions, searching, updating, and deleting.
    """

    def __init__(self):
        self.es = None
        self.connect()

    def connect(self):
        """Establishes a connection to Elasticsearch."""
        try:
            self.es = Elasticsearch(
                [os.getenv("ELASTICSEARCH_HOST")],
                basic_auth=(os.getenv("ELASTICSEARCH_USER"), os.getenv("ELASTICSEARCH_PASSWORD"))
            )
            if self.es.ping():
                print("✅ Connected to Elasticsearch")
            else:
                print("❌ Elasticsearch ping failed")
        except Exception as e:
            print(f"❌ Failed to connect to Elasticsearch: {e}")
            self.es = None

    def index_document(self, index: str, doc_id: str, document: dict):
        """
        Caches a document in Elasticsearch.
        """
        try:
            response = self.es.index(index=index, id=doc_id, document=document)
            return response
        except Exception as e:
            print(f"❌ Error indexing document: {e}")
            return None

    def get_document(self, index: str, doc_id: str):
        """
        Retrieves a document from Elasticsearch (cache).
        """
        try:
            response = self.es.get(index=index, id=doc_id)
            return response["_source"]
        except Exception:
            return None  # If not found, return None

    def update_document(self, index: str, doc_id: str, update_fields: dict):
        """
        Updates fields in Elasticsearch cache.
        """
        try:
            response = self.es.update(index=index, id=doc_id, doc={"doc": update_fields})
            return response
        except Exception as e:
            print(f"❌ Error updating document: {e}")
            return None

    def delete_document(self, index: str, doc_id: str):
        """
        Removes a document from Elasticsearch cache.
        """
        try:
            response = self.es.delete(index=index, id=doc_id)
            return response
        except Exception:
            return None  # Ignore missing cache entries


elasticsearch_service = ElasticsearchService()
