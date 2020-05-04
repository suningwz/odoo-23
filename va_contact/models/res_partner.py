import logging

from odoo import api, fields, models

from .. import exceptions

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):

    _inherit = "res.partner"

    @api.onchange('lastname')
    def _onchange_lastname(self):
        #For individuals, we force the lastname in capital
        if self.lastname and not self.is_company:
            self.lastname = self.lastname.upper()
        else:
            self.lastname = self.lastname