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
                decoded_data = base64.b64decode(doc.attachment_id.datas)
                data = io.StringIO(decoded_data.decode("utf-8"))
                data.seek(0)
                file_reader = []
                csv_reader = csv.reader(data, delimiter=',')
                file_reader.extend(csv_reader)
                _logger.info("{}".format(decoded_data))

