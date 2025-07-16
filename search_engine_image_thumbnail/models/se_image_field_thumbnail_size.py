# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from odoo.osv.expression import FALSE_DOMAIN

class SeImageFieldThumbnailSize(models.Model):
    _name = "se.image.field.thumbnail.size"
    _description = "Index Thumbnail Size"
    display_name = fields.Char(
        compute="_compute_display_name",
        store=True,
    )
    size_ids = fields.Many2many(
        "se.thumbnail.size",
    )
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        domain=lambda self: self._model_id_domain(),
        ondelete="cascade",
    )
    model = fields.Char(
        related="model_id.model",
        string="Model name",
        readonly=True,
        store=True,
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        string="Images field",
        required=True,
        domain="[('model_id', '=', model_id)]",
        ondelete="cascade",
    )
    field_name = fields.Char(
        related="field_id.name",
        string="Field name",
        readonly=True,
        store=True,
    )
    backend_id = fields.Many2one(
        "se.backend",
        string="Backend",
        required=True,
        ondelete="cascade",
    )
    field_id_domain = fields.Binary(
        string="Domain to select images field",
        compute="_compute_field_id_domain",
        readonly=True,
    )
    @api.depends("size_ids", "model_id", "field_id")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.model}.{record.field_name} ({', '.join(record.size_ids.mapped('name'))})"
    @api.model
    def _model_id_domain(self):
        return []
    @api.depends("model_id")
    def _compute_field_id_domain(self):
        for record in self:
            if not record.model_id:
                record.field_id_domain = FALSE_DOMAIN
                continue
            domain_fields = []
            if record.model_id:
                model = self.env[record.model_id.model]
                domain_fields = model._fields.values()
            names = []
            for field in domain_fields:
                if self._is_field_valid_for_thumbnail(field):
                    names.append(field.name)
            record.field_id_domain = (
                [("name", "in", names), ("model_id", "=", record.model_id.id)]
                if names
                else FALSE_DOMAIN
            )
    @api.model
    def _is_field_valid_for_thumbnail(self, field: fields.Field):
        if isinstance(field, fields.Image) or getattr(field, "type", None) == "fs_image":
            return True
        if not getattr(field, "comodel_name", None):
            return False
        if field.comodel_name not in self.env:
            return False
        abstract = self.env["fs.image.relation.mixin"]
        model = self.env[field.comodel_name]
        return isinstance(model, abstract.__class__)
