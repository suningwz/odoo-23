#-*- coding: utf-8 -*-

from odoo import models, fields, api,_

class SafetyAuditElement(models.Model):
    _name = 'safety.audit.element'
    _description = 'Safety Audit Elements'

    active = fields.Boolean(default=True)
    name = fields.Char()
    description = fields.Text()