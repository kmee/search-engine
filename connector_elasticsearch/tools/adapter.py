# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import time
from typing import Any, Iterator
from odoo import _
from odoo.exceptions import UserError
from odoo.addons.connector_search_engine.tools.adapter import SearchEngineAdapter

_logger = logging.getLogger(__name__)

try:
    import elasticsearch
    import elasticsearch.helpers
except ImportError:
    _logger.debug("Can not import elasticsearch")


def _is_delete_nonexistent_documents(elastic_exception):
    b = lambda d: "delete" in d and d["delete"]["status"] == 404  # noqa
    return all(b(error) for error in elastic_exception.errors)


class ElasticSearchAdapter(SearchEngineAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__es_client = None

    @property
    def _index_name(self):
        return self.index_record.name.lower()

    @property
    def _es_connection_class(self):
        return elasticsearch.RequestsHttpConnection

    def create_index(self):
        """Create the index in Elasticsearch."""
        self._es_client.indices.create(index=self._index_name, ignore=400)

    def delete_index(self):
        """Delete the index from Elasticsearch."""
        self._es_client.indices.delete(index=self._index_name, ignore=[400, 404])

    def index_document(self, doc_id, doc_body):
        """Index a document in Elasticsearch."""
        self._es_client.index(index=self._index_name, id=doc_id, body=doc_body)

    def delete_document(self, doc_id):
        """Delete a document from Elasticsearch."""
        self._es_client.delete(index=self._index_name, id=doc_id, ignore=[400, 404])

    def search(self, query, **kwargs):
        """Search documents in Elasticsearch."""
        response = self._es_client.search(index=self._index_name, body=query, **kwargs)
        return response.get("hits", {}).get("hits", [])

    def bulk_index(self, actions):
        """Perform bulk index operation in Elasticsearch."""
        elasticsearch.helpers.bulk(self._es_client, actions, index=self._index_name)

    def bulk_delete(self, actions):
        """Perform bulk delete operation in Elasticsearch."""
        elasticsearch.helpers.bulk(self._es_client, actions, index=self._index_name, raise_on_error=False)

    def get_document(self, doc_id):
        """Get a document from Elasticsearch."""
        try:
            response = self._es_client.get(index=self._index_name, id=doc_id)
            return response["_source"]
        except elasticsearch.exceptions.NotFoundError:
            return None

    def update_document(self, doc_id, doc_body):
        """Update a document in Elasticsearch."""
        self._es_client.update(index=self._index_name, id=doc_id, body={"doc": doc_body})

    def count_documents(self, query):
        """Count documents in Elasticsearch."""
        response = self._es_client.count(index=self._index_name, body=query)
        return response.get("count", 0)
