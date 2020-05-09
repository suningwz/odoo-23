import logging

from odoo import api, fields, models, _
import csv

_logger = logging.getLogger(__name__)

class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def _import_csv(self):
        _logger.info("This is a test")
        pass

