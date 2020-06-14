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
                #_logger.info("Prev {} | New {}".format(prev_social_reason,social_reason))
                self.name = self.name.split(prev_social_reason)[0] + social_reason
            else:
                pass
        else:
            pass
    
    @api.onchange('social_reason_id')
    def _onchange_social_reason_id(self):
        if self.is_company:
            prev = self._origin
            #we manage the case of setting a social reason
            if self.social_reason_id and not prev.social_reason_id:
                #_logger.info("New Case")
                if self.social_reason_id.add_to_name:
                    new_name = self.with_context(lang=self.lang).social_reason_id.name
                    self.name = self.find_and_split(new_name,self.name) + " " + new_name
            
            # we remove the social reason
            elif prev.social_reason_id and not self.social_reason_id:
                #_logger.info("Remove Case")
                old_name = prev.with_context(lang=self.lang).social_reason_id.name
                self.name = self.find_and_split(old_name,self.name)
            
            else:
                #_logger.info("Normal Case")
                #normal change
                old_name = prev.with_context(lang=self.lang).social_reason_id.name
                new_name = self.with_context(lang=self.lang).social_reason_id.name
                temp = self.find_and_split(old_name,self.name)
                #_logger.info("{} removed from {} output {}".format(old_name,self.name,temp))
                if self.social_reason_id.add_to_name:
                    self.name = self.find_and_split(new_name,temp) + " " + new_name
                    #_logger.info("{} added to {} output {}".format(new_name,temp,self.name))
                else:
                    self.name = temp
        else:
            pass
            
    def find_and_split(self,search=False,string=False):
        if search and string:
            found = string.lower().find(search.lower()) 
            if found > 0:
                output = string[:found-1] + string[found+len(search):]
                #_logger.info("{} found in {} output {}".format(search,string,output))
                return output
            else:
                #_logger.info("{} not found in {}".format(search,string))
                return string
        else:
            return string
    
    @api.model
    def name_to_social_reason(self):
        #format (string to search, social reason name in fr_CH, lang)
        SEARCH_LANG = ('fr_CH','de_CH','en_US')
        SOCIAL_REASON_LANG = [
            (' SARL','Sàrl','fr_CH'),
            (' Sàrl','Sàrl','fr_CH'),
            (' Sarl','Sàrl','fr_CH'),
            (' GMBH','Sàrl','de_CH'),
            (' GmbH','Sàrl','de_CH'),
            (' SA','SA','fr_CH'),
            (' AG','SA','de_CH'),
        ]

        to_process = self.search([('social_reason_id','=',False),('is_company','=',True),('comment','ilike','Origin Name | ')])
        for comp in to_process:
            name = comp.comment[14:]
            for conf in SOCIAL_REASON_LANG:
                if conf[0] in name: #we have found a match
                    comp.name = name
                    comp.social_reason_id = self.env['res.partner.social.reason'].search([('name','=',conf[1])],limit=1)
                    comp._onchange_social_reason_id()
                    _logger.info("{} updated in {}, social reason {}".format(name,comp.name,comp.social_reason_id.name))
                    break
                else:
                    pass


