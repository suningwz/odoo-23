# -*- coding: utf-8 -*-
{
    'name': "va_project",

    'summary': """
        Vertical-Access Project customs""",

    'description': """
        Vertical-Access Project customs
    """,

    'author': "Vertical Access Sàrl",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Vertical-Access',
    'version': '0.7.4',


    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'project',
        'project_task_default_stage',
        'project_category',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/project_type_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
