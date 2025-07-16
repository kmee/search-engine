# Copyright 2013 Akretion (http://www.akretion.com)
# Copyright 2021 Camptocamp (http://www.camptocamp.com)
# Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
import logging
import traceback
from collections import defaultdict
from typing import Any, Dict, Iterator

from psycopg2.errors import Error
from typing_extensions import Self

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import identity_exact

from ..tools.json_comparer import compare_json

_logger = logging.getLogger(__name__)

class SeBinding(models.Model):
    _name = "se.binding"
    _description = "Search Engine Record"
    _order = "res_model, res_id desc"
    backend_id = fields.Many2one(
        "se.backend",
        related="index_id.backend_id",
        string="Search Engine Backend",
        store=True,
        readonly=True,
    )
    index_id = fields.Many2one(
        "se.index",
        string="Index",
        required=True,
        ondelete="cascade",
        readonly=True,
    )
    state = fields.Selection(
        [
            ("to_recompute", "To recompute"),
            ("recomputing", "Recomputing"),
            ("to_export", "To export"),
            ("exporting", "Exporting"),
            ("done", "Done"),
            ("invalid_data", "Invalid Data"),
            ("recompute_error", "Fail to Recompute"),
            ("to_delete", "To Delete"),
            ("deleting", "Deleting"),
        ],
        string="State",
        default="to_recompute",
        required=True,
        index=True,
    )
    res_model = fields.Char(
        string="Resource Model",
        required=True,
        index=True,
        help="Model of the resource that is indexed in the search engine",
    )
    res_id = fields.Integer(
        string="Resource ID",
        required=True,
        index=True,
        help="ID of the resource that is indexed in the search engine",
    )
    create_date = fields.Datetime(
        string="Creation Date", readonly=True, help="Date when the record was created"
    )
    write_date = fields.Datetime(
        string="Last Modification Date",
        readonly=True,
        help="Date when the record was last modified",
    )
    json_data = fields.Text(
        string="JSON Data",
        help="Data in JSON format that represents the indexed resource",
    )
    error_message = fields.Text(
        string="Error Message",
        readonly=True,
        help="Error message in case of failure during recompute or export",
    )
    retry_count = fields.Integer(
        string="Retry Count",
        default=0,
        help="Number of times the recompute or export has been retried",
    )
    binding_type = fields.Selection(
        [
            ("document", "Document"),
            ("alias", "Alias"),
        ],
        string="Binding Type",
        default="document",
        required=True,
        help="Type of binding for the search engine record",
    )
    record_id = fields.Many2one(
        "se.indexable.record",
        string="Indexable Record",
        required=True,
        ondelete="cascade",
        help="Referência ao registro indexável relacionado a este binding."
    )
    date_recomputed = fields.Datetime(readonly=True)
    date_synchronized = fields.Datetime(readonly=True)

    @api.model
    def _get_indexable_model_selection(self):
        return [
            (model, self.env[model]._description)
            for model in self.env
            if (
                hasattr(self.env[model], "_se_indexable")
                and not self.env[model]._abstract
                and not self.env[model]._transient
            )
        ]
