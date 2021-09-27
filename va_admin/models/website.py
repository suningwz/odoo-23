# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class Website(models.AbstractModel):
    _inherit = "website"

    external_link = fields.Char()

    """def _get_external_link(self):
        self.ensure_one()
        url_params = {
            'id': self.id,
            'view_type': 'form',
            'model': 'your_model',
            'menu_id': self.env.ref('module_name.menu_record_id').id,
            'action': self.env.ref('module_name.action_record_id').id,
        }
        params = '/web?#%s' % url_encode(url_params)
        return base_url + params"""