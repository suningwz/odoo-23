# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = "sale.order"

    #we do custom numbering for our sales orders
    seq_ref = fields.Char(
        readonly=True,
        string= "Reference",
    )

    #we create more employee/contact related fields in the sale order to cope with specific needs
    # we create a dedicated contact on the client side, which is different of all existing addresses
    your_contact_id = fields.Many2one(
        comodel_name='res.partner',
    )
    #we create the business unit in order to cope with the need of custom header on layouts
    business_unit_id = fields.Many2one(
        comodel_name='res.partner',
        domain = [('is_company','=',True)],
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

        if 'name' in vals:
            vals['name'] = "{} | {}".format(vals['seq_ref'],vals['name'])
        result = super(SaleOrder, self).create(vals)
        return result

class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"
    
    #we override this because we don't want the price to be updated anymore when we change the ordered qty
    #@api.onchange('product_uom', 'product_uom_qty')
    @api.onchange('product_uom')
    def product_uom_change(self):
        super(SaleOrderLine, self).product_uom_change()
        """if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)"""
