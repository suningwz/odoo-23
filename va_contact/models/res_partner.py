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
            pass

    ### CUSTOM NAMING
    ### The 3 below methods are designed to automatically add the social reason
    ### at the end of the comany name, in the language of the partner
    
    @api.onchange('name')
    def _onchange_name(self):
        if self.is_company and self.social_reason_id:
            social_reason = (" " + self.with_context(lang=self.lang).social_reason_id.name)
            self.name = self.name.split(social_reason)[0] + social_reason
        else:
            pass
    
    @api.onchange('lang')
    def _onchange_lang(self):
        if self.is_company and self.social_reason_id:
            prev = self._origin
            prev_social_reason = (" " + self.with_context(lang=prev.lang).social_reason_id.name)
            social_reason = (" " + self.with_context(lang=self.lang).social_reason_id.name)
            _logger.info("Prev {} | New {}".format(prev_social_reason,social_reason))
            self.name = self.name.split(prev_social_reason)[0] + social_reason
        else:
            pass
    
    @api.onchange('social_reason_id')
    def _onchange_social_reason_id(self):
        if self.is_company and self.social_reason_id:
            prev = self._origin
            prev_social_reason = (" " + prev.with_context(lang=self.lang).social_reason_id.name)
            social_reason = (" " + self.with_context(lang=self.lang).social_reason_id.name)
            _logger.info("Prev {} | New {}".format(prev_social_reason,social_reason))
            self.name = self.name.split(prev_social_reason)[0] + social_reason
        else:
            pass

