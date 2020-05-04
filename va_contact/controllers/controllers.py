# -*- coding: utf-8 -*-
# from odoo import http


# class VaContact(http.Controller):
#     @http.route('/va_contact/va_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/va_contact/va_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('va_contact.listing', {
#             'root': '/va_contact/va_contact',
#             'objects': http.request.env['va_contact.va_contact'].search([]),
#         })

#     @http.route('/va_contact/va_contact/objects/<model("va_contact.va_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('va_contact.object', {
#             'object': obj
#         })
