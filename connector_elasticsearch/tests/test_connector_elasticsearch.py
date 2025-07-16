# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
from time import sleep
from vcr_unittest import VCRMixin
from odoo.tools import mute_logger
from odoo.addons.connector_search_engine.tests.test_all import TestBindingIndexBase
from ..tools.adapter import ElasticSearchAdapter


class TestConnectorElasticsearch(VCRMixin, TestBindingIndexBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend = cls.env.ref("connector_elasticsearch.backend_1")
        cls.setup_records()
        cls.adapter: ElasticSearchAdapter = cls.se_index.se_adapter

    def _get_vcr_kwargs(self, **kwargs):
        return {
            "record_mode": "one",
            "match_on": ["method", "path", "query"],
            "filter_headers": ["Authorization"],
            "decode_compressed_response": True,
        }

    @classmethod
    def setup_records(cls):
        cls.se_config = cls.env["se.index.config"].create(
            {"name": "my_config", "body": {"mappings": {}}}
        )
