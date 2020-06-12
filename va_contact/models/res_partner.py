import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class SocialReason(models.Model):
    _name = 'res.partner.social.reason'
    _description = 'Company Social Reason'

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    add_to_name = fields.Boolean(default=True,string=_('Add to Contact Name'))

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
    ### at the end of the comany name, if 'add_to_name' is True, in the language of the partner
    
    @api.onchange('name')
    def _onchange_name(self):
        if self.is_company and self.social_reason_id:
            if self.social_reason_id.add_to_name:
                social_reason = (" " + self.with_context(lang=self.lang).social_reason_id.name)
                self.name = self.name.split(social_reason)[0] + social_reason
            else:
                pass
        else:
            pass
    
    @api.onchange('lang')
    def _onchange_lang(self):
        if self.is_company and self.social_reason_id:
            if self.social_reason_id.add_to_name:
                prev = self._origin
                prev_social_reason = (" " + self.with_context(lang=prev.lang).social_reason_id.name)
                social_reason = (" " + self.with_context(lang=self.lang).social_reason_id.name)
                _logger.info("Prev {} | New {}".format(prev_social_reason,social_reason))
                self.name = self.name.split(prev_social_reason)[0] + social_reason
            else:
                pass
        else:
            pass
    
    @api.onchange('social_reason_id')
    def _onchange_social_reason_id(self):
        prev = self._origin
        #we manage the case of setting a social reason
        if self.is_company and self.social_reason_id and not prev.social_reason_id:
            if self.social_reason_id.add_to_name:
                new_name = self.with_context(lang=self.lang).social_reason_id.name
                self.name = self.find_and_split(new_name,self.name) + " " + new_name
        
        # we remove the social reason
        elif prev.social_reason_id and not self.social_reason_id:
            old_name = prev.with_context(lang=self.lang).social_reason_id.name
            self.name = self.find_and_split(old_name,self.name)
        
        else:
            #normal change
            old_name = prev.with_context(lang=self.lang).social_reason_id.name
            new_name = self.with_context(lang=self.lang).social_reason_id.name
            temp = self.find_and_split(old_name,self.name)
            if self.social_reason_id.add_to_name:
                self.name = temp + " " + new_name
            else:
                self.name = temp
            
    def find_and_split(self,search=False,string=False):
        if search and string:
            found = string.lower().find(search.lower()) 
            if found > 0:
                output = string[:found] + string[found+len(search):]
                _logger.info("{} found in {} output {}".format(search,string,output))
                return output
            else:
                return string
        else:
            return string

