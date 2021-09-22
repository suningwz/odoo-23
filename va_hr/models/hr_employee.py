# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class Employee(models.Model):

    _inherit = "hr.employee"

    short_name = fields.Char(
        compute = '_compute_short_name',
        store = True,
    )

    @api.depends('address_id.firstname','address_id.lastname')
    def _compute_short_name(self):
        for emp in self:
            _logger.info(emp.name)
            if emp.address_id and emp.address_id.firstname and emp.address_id.lastname:
                emp.short_name = (emp.address_id.firstname[:1] + emp.address_id.lastname[:2]).upper()
            else:
                emp.short_name = False