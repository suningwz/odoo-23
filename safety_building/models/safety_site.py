#-*- coding: utf-8 -*-

from odoo import models, fields, api,_

class SafetySiteArea(models.Model):
    _name = 'safety.site.area'
    _description = 'Safety Site Area'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean()
    name = fields.Char()
    description = fields.Text()
    site_id = fields.Many2one(
        comodel_name = 'safety.site',
        required = True,
    )
    external_resp_id = fields.Many2one(
        comodel_name = 'res.partner',
    )
    internal_resp_id = fields.Many2one(
        comodel_name = 'res.users',
    )

class SafetySite(models.Model):
    _name = 'safety.site'
    _description = 'Safety Site'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    description = fields.Text()

    partner_id = fields.Many2one(
        compdel_name = 'res.partner',
        domain = [('is_company','=',True)],
        required = True,
        help = _('The company owning the audited building site.')
    )

    external_resp_id = fields.Many2one(
        comodel_name = 'res.partner',
        domain = [('is_company','=',False)]
    )

    internal_resp_id = fields.Many2one(
        comodel_name = 'res.users',
    )

    site_area_ids = fields.One2many(
        comodel_name = 'safety.site.area',
        inverse_name = 'site_id',
    )




