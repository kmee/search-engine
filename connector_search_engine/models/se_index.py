# Copyright 2013 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict
from typing import List

from odoo import _, api, fields, models

from odoo.addons.queue_job.job import identity_exact

from ..tools.adapter import SearchEngineAdapter
from ..tools.serializer import ModelSerializer
from ..tools.validator import DefaultJsonValidator, JsonValidator

_logger = logging.getLogger(__name__)

class SeIndex(models.Model):
    _name = "se.index"
    _description = "Se Index"
    __slots__ = ("_se_adapter", "_model_serializer", "_json_validator")
    name = fields.Char(compute="_compute_name", store=True)
    custom_tech_name = fields.Char(
        help="Take control of index technical name. "
        "The final index name is still computed and contains in any case: "
        "backend index name prefix and language if given. "
        "If no custom name is provided, model's normalized name will be used."
    )
    backend_id = fields.Many2one(
        "se.backend", string="Backend", required=True, ondelete="cascade"
    )
    lang_id = fields.Many2one("res.lang", string="Lang", required=False)
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        domain=lambda self: self._model_id_domain(),
        ondelete="cascade",
    )
    serializer_type = fields.Selection([])
    batch_exporting_size = fields.Integer(
        default=1000, help="Batch size for exporting element"
    )
    batch_recomputing_size = fields.Integer(
        default=50, help="Batch size for recomputing element"
    )
    config_id = fields.Many2one(
        comodel_name="se.index.config",
        string="Config",
        help="Index configuration record",
    )
    binding_ids = fields.One2many("se.binding", "index_id", "Binding")
    color = fields.Integer(string="Color Index", compute="_compute_count_binding")
    count_done = fields.Integer(compute="_compute_count_binding")
    count_pending = fields.Integer(compute="_compute_count_binding")
    count_error = fields.Integer(compute="_compute_count_binding")
    count_all = fields.Integer(compute="_compute_count_binding")
    model_serializer = fields.Serialized(
        string="Model Serializer",
        compute="_compute_model_serializer",
        store=False,
    )

    @api.model
    def _model_id_domain(self):
        se_model_names = [
            x[0] for x in self.env["se.binding"]._get_indexable_model_selection()
        ]
        return [("model", "in", se_model_names)]

    @api.depends("binding_ids.state")
    def _compute_count_binding(self):
        from collections import defaultdict
        res = defaultdict(lambda: defaultdict(int))
        data = self.env["se.binding"].read_group(
            [
                ("index_id", "in", self.ids),
            ],
            ["index_id", "state"],
            groupby=["index_id", "state"],
            lazy=False,
        )
        _all = 0
        for item in data:
            count = item["__count"]
            res[item["index_id"][0]][item["state"]] = count
            _all += count
        def get(index_id, states):
            return sum([res[index_id][state] for state in states])
        for record in self:
            record.count_done = get(record.id, ["done"])
            record.count_pending = get(
                record.id,
                [
                    "to_recompute",
                    "recomputing",
                    "to_export",
                    "exporting",
                    "to_delete",
                    "deleting",
                ],
            )
            record.count_error = get(record.id, ["invalid_data", "recompute_error"])
            record.count_all = _all
            if record.count_error:
                record.color = 1
            elif record.count_pending:
                record.color = 2
            else:
                record.color = 10

    @api.depends("serializer_type")
    def _compute_model_serializer(self):
        for rec in self:
            rec.model_serializer = rec.model_serializer if hasattr(rec, "model_serializer") else None

    def force_recompute_all_binding(self):
        from odoo.exceptions import UserError
        raise UserError("Método force_recompute_all_binding chamado. Implemente a lógica ou remova o botão da view se não for necessário.")

    def force_batch_sync(self):
        from odoo.exceptions import UserError
        raise UserError("Método force_batch_sync chamado. Implemente a lógica ou remova o botão da view se não for necessário.")

    def export_settings(self):
        from odoo.exceptions import UserError
        raise UserError("Método export_settings chamado. Implemente a lógica ou remova o botão da view se não for necessário.")

    def clear_index(self):
        from odoo.exceptions import UserError
        raise UserError("Método clear_index chamado. Implemente a lógica ou remova o botão da view se não for necessário.")

    def reindex(self):
        from odoo.exceptions import UserError
        raise UserError("Método reindex chamado. Implemente a lógica ou remova o botão da view se não for necessário.")

    def action_open_bindings(self):
        from odoo.exceptions import UserError
        raise UserError("Método action_open_bindings chamado. Implemente a lógica ou remova o botão da view se não for necessário.")
