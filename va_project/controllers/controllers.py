# -*- coding: utf-8 -*-
# from odoo import http


# class VaProject(http.Controller):
#     @http.route('/va_project/va_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/va_project/va_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('va_project.listing', {
#             'root': '/va_project/va_project',
#             'objects': http.request.env['va_project.va_project'].search([]),
#         })

#     @http.route('/va_project/va_project/objects/<model("va_project.va_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('va_project.object', {
#             'object': obj
#         })
