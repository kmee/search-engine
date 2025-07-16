# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from contextlib import contextmanager
from odoo import fields, models
from ..tools.adapter import SearchEngineAdapter
class FakeSeAdapter(SearchEngineAdapter):
    def __init__(self, *args):
        super().__init__(*args)
        if not hasattr(self, "_mocked_calls"):
            self._mocked_calls = []
    def index(self, data):
        self._mocked_calls.append(
            dict(index=self.index_record, method="index", args=data)
        )
    def delete(self, binding_ids):
        self._mocked_calls.append(
            dict(index=self.index_record, method="delete", args=binding_ids)
        )
    def clear(self):
        self._mocked_calls.append(
            dict(index=self.index_record, method="clear", args=None)
        )
    def each(self):
        self._mocked_calls.append(
            dict(index=self.index_record, method="each", args=None)
        )
        return [{"id": 42}]
    @classmethod
    @contextmanager
    def mocked_calls(cls):
        calls = []
        yield calls
