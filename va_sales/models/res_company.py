# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Company(models.Model):

    _inherit = "res.company"

    #we do custom numbering for our sales orders
    business_unit_ids = fields.Many2many(
        comodel_name = 'res.partner',
        domain = [('is_company','=',True)],
    )

