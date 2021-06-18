# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EventEvent(models.Model):

    _inherit = "event.event"

    is_private = fields.Boolean(default=False)
    
    reporting_event_type_id = fields.Many2one(
        comodel_name = "event.type",
        compute = "_compute_reporting_event_type",
        store = True,
        string = "Reporting Template",
    )

    @api.depends('event_type_id','event_type_id.parent_id')
    def _compute_reporting_event_type(self):
        for event in self:
            if not event.event_type_id:
                event.reporting_event_type_id = False
            else:
                event.reporting_event_type_id = event.event_type_id.parent_id if event.event_type_id.parent_id else event.event_type_id