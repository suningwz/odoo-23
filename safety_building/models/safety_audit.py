#-*- coding: utf-8 -*-

from odoo import models, fields, api,_

class SafetyAudit(models.Model):
    _name = 'safety.audit'
    _description = 'Safety Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True)
    name = fields.Char()
    description = fields.Text()
    site_id = fields.Many2one(
        comodel_name = 'safety.site',
        required = True,
    )
    
    auditor_ids = fields.Many2many(
        comodel_name = 'res.users',
    )

    date_start = fields.Date()
    date_end = fields.Date()

    status = fields.Selection(
        selection = [
            ('planned',_('Planned')),
            ('ongoing',_('Ongoing')),
            ('done',_('Done')),
            ('cancelled',_('Cancelled')),
        ]
    )

    element_ids = fields.Many2many(
        comodel_name = 'safety.audit.element'
    )

    @api.onchange('site_id')
    def _onchange_site(self):
        self.element_ids = self.site_id.default_element_ids if self.site_id else False