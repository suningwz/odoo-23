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

    description = fields.Text()
    responsible_id = fields.Many2one(
        comodel_name = 'res.partner',
    )

    image = fields.Image()

    objectives = fields.Html()
    requirements = fields.Html()

    price = fields.Float()