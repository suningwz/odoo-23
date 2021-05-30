# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EventType(models.Model):

    _inherit = "event.type"

    active = fields.Boolean(default=True)
    category = fields.Selection(
        selection = [
            ('architecture','Architecture'),
            ('sst','SST'),
            ('technique','Technique'),],
    )
    subtitle = fields.Text()
    description = fields.Text()
    responsible_id = fields.Many2one(
        comodel_name = 'res.partner',
    )
    responsible_info = fields.Text(
        compute = '_compute_responsible_info',
        store = True,
    )

    @api.depends('responsible_id')
    def _compute_responsible_info(self):
        for type in self:
            if type.responsible_id:
                type.responsible_info = '{}\n{}\n{}\n{}'.format(type.responsible_id.name,type.responsible_id.function,type.responsible_id.phone,type.responsible_id.email)
            else:
                type.responsible_info = 'à définir'

    image = fields.Image()

    objectives = fields.Html()
    requirements = fields.Html()

    price_info = fields.Html()