# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Invoice(models.Model):

    _inherit = "account.move"

    comment = fields.Char()
    
    # we create a dedicated contact on the client side, which is different of all existing addresses
    your_contact_id = fields.Many2one(
        comodel_name='res.partner',
    )
    # we create a dedicated contact as sales referee  
    referee_id = fields.Many2one(
        comodel_name='res.partner',
    )
    #we create the business unit in order to cope with the need of custom header on layouts
    business_unit_id = fields.Many2one(
        comodel_name='res.partner',
        domain = [('is_company','=',True)],
    )

