# -*- coding: utf-8 -*-
# from odoo import http


# class SecurityAudit(http.Controller):
#     @http.route('/security_audit/security_audit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_audit/security_audit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_audit.listing', {
#             'root': '/security_audit/security_audit',
#             'objects': http.request.env['security_audit.security_audit'].search([]),
#         })

#     @http.route('/security_audit/security_audit/objects/<model("security_audit.security_audit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_audit.object', {
#             'object': obj
#         })
