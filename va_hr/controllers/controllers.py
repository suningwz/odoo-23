# -*- coding: utf-8 -*-
# from odoo import http


# class VaHr(http.Controller):
#     @http.route('/va_hr/va_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/va_hr/va_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('va_hr.listing', {
#             'root': '/va_hr/va_hr',
#             'objects': http.request.env['va_hr.va_hr'].search([]),
#         })

#     @http.route('/va_hr/va_hr/objects/<model("va_hr.va_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('va_hr.object', {
#             'object': obj
#         })
