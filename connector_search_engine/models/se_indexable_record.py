# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from lxml import etree

from odoo import api, fields, models

if TYPE_CHECKING:
    from .se_binding import SeBinding
    from .se_index import SeIndex

SMART_BUTTON = """
<button class="oe_stat_button"
       name="open_se_binding"
       icon="fa-list-ul"
       type="object"
       attrs="{'invisible': [('count_se_binding_total', '=', 0)]}">
       <div class="o_field_widget o_stat_info">
            <field name="count_se_binding_total" invisible="1"/>
            <span class="o_stat_value">
                <i attrs="{'invisible': [
                    '|',
                    ('count_se_binding_pending', '>', 0),
                    ('count_se_binding_error', '>', 0)
                   ]}"
                   class="fa fa-thumbs-o-up text-success o_column_title"
                   aria-hidden="true"> :
                    <field name="count_se_binding_done"/>
                </i>
                <i attrs="{'invisible': [
                    '|',
                    ('count_se_binding_pending', '=', 0),
                    ('count_se_binding_error', '>', 0)
                   ]}"
                   class="fa fa-spinner text-warning" aria-hidden="true"> :
                    <field name="count_se_binding_pending"/>
                </i>
                <i attrs="{'invisible': [('count_se_binding_error', '=', 0)]}"
                   class="fa fa-exclamation-triangle text-danger" aria-hidden="true"> :
                    <field name="count_se_binding_error"/>
                </i>
            </span>
            <span>Index</span>
       </div>
</button>"""

class SeIndexableRecord(models.AbstractModel):
    _name = "se.indexable.record"
    _description = "Mixin that make record indexable in a search engine"
    _se_indexable = True
    se_binding_ids = fields.One2many(
        string="Seacrh Engine Bindings",
        comodel_name="se.binding",
        inverse_name="record_id",
    )
