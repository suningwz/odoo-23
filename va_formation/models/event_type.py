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

    @api.depends('responsible_id','responsible_id.name','responsible_id.function','responsible_id.mobile','responsible_id.phone','responsible_id.email')
    def _compute_responsible_info(self):
        for type in self:
            if type.responsible_id:
                type.responsible_info = '{}\n{}\n{}\n{}'.format(type.responsible_id.name,type.responsible_id.function,type.responsible_id.mobile or type.responsible_id.phone,type.responsible_id.email)
            else:
                type.responsible_info = 'à définir'

    image = fields.Image()

    objectives = fields.Text(
        help = "Use || as separator to generate a new bullet in WordPress"
    )
    requirements = fields.Text(
        help = "Use || as separator to generate a new bullet in WordPress"
    )

    price_single = fields.Float()
    price_group = fields.Float()