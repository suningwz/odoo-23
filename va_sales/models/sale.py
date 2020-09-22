# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = "sale.order"

    seq_ref = fields.Char(
        readonly=True,
        string= "Reference",
    )

    @api.model
    def create(self, vals):
        seq_date = None
        if 'date_order' in vals:
            seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
        if 'company_id' in vals:
            vals['seq_ref'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                'sale.order', sequence_date=seq_date) or _('New')
        else:
            vals['seq_ref'] = self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')

        vals['name'] = "{} | {}".format(vals['seq_ref'],vals['name'])
        result = super(SaleOrder, self).create(vals)
        return result
