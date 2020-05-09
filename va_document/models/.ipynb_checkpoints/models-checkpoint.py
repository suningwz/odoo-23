# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class va_contact(models.Model):
#     _name = 'va_contact.va_contact'
#     _description = 'va_contact.va_contact'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
