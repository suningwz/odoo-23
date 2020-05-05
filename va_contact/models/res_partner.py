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
        comodel_name='res.partner.social.reason',
    )

    @api.onchange('lastname')
    def _onchange_lastname(self):
        #For individuals, we force the lastname in capital
        if self.lastname and not self.is_company:
            self.lastname = self.lastname.upper()
        else:
            self.lastname = self.lastname
    
    #just to trigger comptation based on social_reason_id
    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name','social_reason_id','lang')
    def _compute_display_name(self):
        super(ResPartner,self)._compute_display_name()
        for partner in self.filtered(lambda p: p.is_company and p.social_reason_id):
            partner.display_name = "{} {}".format(partner.name,partner.with_context(lang=partner.lang).social_reason_id.name)