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
        stages = self.env["project.task.type"].search([("case_default", "=", True),("default_project_type_id", "=", project_type_id)])
        if stages:
            vals['type_ids'] = [(6,0,stages.ids)]
        return super(Project, self).create(vals)

