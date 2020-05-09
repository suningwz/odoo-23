import logging

from odoo import api, fields, models, _
import csv
import base64

_logger = logging.getLogger(__name__)

class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def _import_csv(self):
        context = self.env.context
        for doc in context.get('active_ids'):
            decoded_data = base64.b64decode(doc.attachment_id)
            _logger.info("{}".format(decoded_data))

