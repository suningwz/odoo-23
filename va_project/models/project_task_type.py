
from odoo import fields, models

class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    default_project_type_id = fields.Many2one(
        comodel_name = "project.type",
        help="Specify for which project category this task type is default.",
    )
