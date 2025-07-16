# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import OrderedDict
from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.addons.connector_search_engine.models.se_index import SeIndex
from odoo.addons.fs_base_multi_image.models.fs_image_relation_mixin import FsImageRelationMixin
from odoo.addons.fs_image.fields import FSImageValue
from odoo.addons.fs_image_thumbnail.models.fs_image_thumbnail_mixin import FsImageThumbnailMixin
from .se_thumbnail_size import SeThumbnailSize
class SeIndexableRecord(models.AbstractModel):
    _inherit = "se.indexable.record"
    def _get_or_create_thumbnails_for_multi_images(self, index: SeIndex, field_name: str) -> OrderedDict:
        """Create a thumbnail for a multi image field.
        :param index: The index where the record should be added
        :param field_name: The name of the field
        :return:  a ordered dictionary where the key is the original image relation and the value is a list of tuple(se.thumbnail.size, se.thumbnail)
            (The order of the dict is the order of the images in the original Odoo record)
        """
        self.ensure_one()
        thumbnail_sizes_by_size = self._get_thumbnail_sizes_by_size_for_field(index, field_name)
        # ...continua conforme o original...
