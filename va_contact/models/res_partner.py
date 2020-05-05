import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class SocialReason(models.Model):
    _name = 'res.partner.social.reason'
    _description = 'Company Social Reason'

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)

class ResPartner(models.Model):

    _inherit = "res.partner"

    social_reason_id = fields.Many2one(
        string=_('Social Reason'),
        comodel_name='res.partner.social.reason',
        #translate = True
    )

    @api.onchange('lastname')
    def _onchange_lastname(self):
        #For individuals, we force the lastname in capital
        if self.lastname and not self.is_company:
            self.lastname = self.lastname.upper()
        else:
            self.lastname = self.lastname