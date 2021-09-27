# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Invoice(models.Model):

    _inherit = "account.move"

    comment = fields.Char()

