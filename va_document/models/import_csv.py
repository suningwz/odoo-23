import logging

from odoo import api, fields, models, _
import csv

_logger = logging.getLogger(__name__)

class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def import_csv(self):
        pass

