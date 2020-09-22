# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class QuotationTemplate(models.Model):

    _inherit = "sale.order.template"

    project_type_id = fields.Many2one(
        comodel_name = "project.type",
        help="Project type is defining default stages at project creation.",
    )

class SaleOrder(models.Model):

    _inherit = "sale.order"

    project_type_id = fields.Many2one(
        comodel_name = "project.type",
        help="Project type is defining default stages",
    )

    @api.onchange('sale_order_template_id')
    def onchange_template_id(self):
        for so in self:
            if so.sale_order_template_id:
                so.project_type_id = so.sale_order_template_id.project_type_id
            else:
                so.project_type_id = False

