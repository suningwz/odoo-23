# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Project(models.Model):

    _name = "project.project"
    _inherit = [
        'project.project',
        'mail.activity.mixin',
        ]

    @api.model
    def create(self, vals):
        project_type_id = vals.get('type_id',False)
        ids = self.env["project.task.type"].search([("case_default", "=", True),("default_project_type_id", "=", project_type_id)])
        if ids:
            vals['type_ids'] = [(6,0,ids)]
        return super(Project, self).create(vals)

