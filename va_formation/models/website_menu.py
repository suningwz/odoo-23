# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class WebsiteMenu(models.Model):

    _inherit = "website.menu"

    active = fields.Boolean(default=True)