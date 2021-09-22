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

    @api.depends('firstname','lastname')
    def _compute_short_name(self):
        for emp in self:
            emp.short_name = (emp.firstname[:1] + emp.lastname[:2]).upper()