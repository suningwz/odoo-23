# -*- coding: utf-8 -*-
# from odoo import http


# class VaSales(http.Controller):
#     @http.route('/va_sales/va_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/va_sales/va_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('va_sales.listing', {
#             'root': '/va_sales/va_sales',
#             'objects': http.request.env['va_sales.va_sales'].search([]),
#         })

#     @http.route('/va_sales/va_sales/objects/<model("va_sales.va_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('va_sales.object', {
#             'object': obj
#         })
