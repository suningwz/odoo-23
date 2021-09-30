# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Company(models.Model):

    _inherit = "res.company"

    business_unit_ids = fields.Many2many(
        comodel_name = 'res.partner',
        domain = [('is_company','=',True)],
        string="Business Units"
    )

class Partner(models.Model):

    _inherit = "res.partner"

    #default referee for this client
    referee_id = fields.Many2one(
        comodel_name = 'res.partner',
        string="Commercial"
    )

