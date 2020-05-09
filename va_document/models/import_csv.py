import logging

from odoo import api, fields, models, _
import csv

_logger = logging.getLogger(__name__)

class Csv(models.Model):
    _name = 'interface.csv'
    _description = 'CSV file'

    document_id = fields.Many2one()