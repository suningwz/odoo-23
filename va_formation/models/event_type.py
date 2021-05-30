# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EventType(models.Model):

    _inherit = "event.type"

    category = fields.Selection(
        selection = [
            ('architecture','Architecture'),
            ('sst','SST'),
            ('technique','Technique'),],
    )