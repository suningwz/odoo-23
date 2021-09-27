# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class Website(models.AbstractModel):
    _inherit = "website"

    external_link = fields.Char()

    def _get_external_link(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.external_link,
            'target': 'self',
            'res_id': self.id,
        }