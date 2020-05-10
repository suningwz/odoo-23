import logging

from odoo import api, fields, models, _
import csv
import io
import base64

_logger = logging.getLogger(__name__)

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
    
    def process_pipedrive_company(self,data=False):
        self.ensure_one()
        if data:
            headers = data.pop(0)
            _logger.info("{}".format(headers))
            out=[]
            for item in data:
                vals = dict(zip(headers,item))
                out.append(vals)
                #_logger.info("{} {}".format(vals['Nom'],vals['Ville/agglomération/village/localité']))
            _logger.info("{}".format(out[0]))
            _logger.info("{}".format(data[0]))



