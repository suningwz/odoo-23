import logging

from odoo import api, fields, models, _
import csv
import io
import base64

_logger = logging.getLogger(__name__)

#format (string to search, social reason name in fr_CH, lang)
SOCIAL_REASON_LANG = [
    (' SA','SA','fr_CH'),
    (' AG','SA','de_CH'),
    (' SARL','SARL','fr_CH'),
    (' Sàrl','SARL','fr_CH'),
    (' GMBH','SARL','de_CH'),
    (' GmbH','SARL','de_CH'),
]

class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def _import_csv(self):
        context = self.env.context
        if context.get('active_ids'):
            docs = self.browse(context['active_ids'])
            for doc in docs:
                if self.env.ref('va_document.doctag_import_contact_pd_company') in doc.tag_ids:
                    doc.process_pipedrive_company(doc.csv_decode(';'))
                else:
                    pass
    

    def csv_decode(self,delimiter=','):
        self.ensure_one()
        decoded_data = base64.b64decode(self.attachment_id.datas)
        data = io.StringIO(decoded_data.decode("utf-8"))
        data.seek(0)
        file_reader = []
        csv_reader = csv.reader(data, delimiter=';')
        file_reader.extend(csv_reader)
        return file_reader
    
    def process_pipedrive_company(self,data=False,force=False):
        self.ensure_one()
        if data:
            headers = data.pop(0)
            _logger.info("{}".format(headers))
            
            #we initiate general values
            vals = {
                'is_company': True,
                'company_type': 'company',
                'company_id': self.env.ref("base.main_company"),
            }

            for item in data:
                name = item[1]
                #we search existing contact notes to find if we already imported this one
                existing = self.env['res.partner'].search([('comment','ilike',name),('is_company','ilike',name)],limit=1)
                if not existing or force:
                    vals.update(self.pipedrive_company_name(name))
                    _logger.info("{}".format(vals))
    
    def pipedrive_company_name(self,name = False):
        self.ensure_one()
        vals={}
        if name:
            #we set default values
            vals.update({
                'comment':'Origin Name | {}'.format(name),
                'social_reason_id': False,
                'lang': 'fr_CH',
                'name': name,
            })
            for conf in SOCIAL_REASON_LANG:
                if conf[0] in name: #we have found a match
                    parts = name.split(conf[0])
                    new_name = "{} {}".format(parts[0],conf[1]) if len(parts)==1 \
                        else "{} {} {}".format(parts[0],parts[1],conf[1])
                    vals.update({
                        'social_reason_id': self.env['res.partner.social.reason'].search([('name','=',conf[1])],limit=1).id,
                        'lang': conf[2],
                        'name': new_name,
                    })
                    break 
        else:
            pass

        return vals
                    



