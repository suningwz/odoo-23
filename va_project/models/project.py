# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Project(models.Model):

    _name = "project.project"
    _inherit = [
        'project.project',
        'mail.activity.mixin',
        ]

#_inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']
#_inherit = ['portal.mixin', 'mail.alias.mixin', 'mail.thread', 'rating.parent.mixin']