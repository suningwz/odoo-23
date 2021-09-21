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

    short_name = fields.Char(
        related = 'event_type_id.short_name',
        store = True,
    )

    city = fields.Char(
        related = 'address_id.city',
        store = True,
    )

    autonaming = fields.Boolean(
        help="If checked, related events will be automatically named based on template info and time/location."
    )

    @api.depends('event_type_id','event_type_id.parent_id')
    def _compute_reporting_event_type(self):
        for event in self:
            if not event.event_type_id:
                event.reporting_event_type_id = False
                event.autonaming = False
            else:
                event.reporting_event_type_id = event.event_type_id.parent_id if event.event_type_id.parent_id else event.event_type_id
                event.autonaming = event.reporting_event_type_id.autonaming
            event._autonaming()

    def _autonaming(self):
        for event in self.filtered(lambda e: e.autonaming):
            if event.reporting_event_type_id:
                event.name = "{} - {}".format(event.reporting_event_type_id.short_name, event.date_begin.date())
                event.subtitle = event.reporting_event_type_id.subtitle
                event.description = event.reporting_event_type_id.description
            else:
                event.name = "Not enough autonaming info."
                event.subtitle = False
                event.description = False
    
    @api.onchange('date_begin')
    def _onchange_date_begin(self):
        self._autonaming()
    
    @api.onchange('address_id')
    def _onchange_address_id(self):
        self._autonaming()
