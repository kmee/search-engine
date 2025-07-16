# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from unittest import mock
from odoo_test_helper import FakeModelLoader
from odoo.exceptions import ValidationError
from odoo.tests.common import Form
from odoo.tools import mute_logger
from odoo.addons.queue_job.job import identity_exact
from odoo.addons.queue_job.tests.common import trap_jobs
from .common import TestSeBackendCaseBase
class TestBindingIndexBase(TestSeBackendCaseBase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import (
            FakeSeAdapter,
            FakeSerializer,
            ResPartner,
            ResUsers,
            SeBackend,
            SeIndex,
        )
        cls.loader.update_registry((ResPartner, ResUsers, SeBackend, SeIndex))
        cls.binding_model = cls.env["se.binding"]
        cls.se_index_model = cls.env["se.index"]
        cls.se_adapter = FakeSeAdapter
        cls.model_serializer = FakeSerializer
