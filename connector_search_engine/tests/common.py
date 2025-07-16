# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from urllib import parse as urlparse
from odoo import tools
from odoo.modules.module import get_resource_path
from odoo.tests.common import TransactionCase

def load_xml(env, module, filepath):
    tools.convert_file(
        env.cr,
        module,
        get_resource_path(module, filepath),
        {},
        mode="init",
        noupdate=False,
        kind="test",
    )
class TestSeBackendCaseBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                tracking_disable=True,
                queue_job__no_delay=True,
            )
        )
    @classmethod
    def _load_fixture(cls, fixture, module="connector_search_engine"):
        load_xml(cls.env, module, "tests/fixtures/%s" % fixture)
