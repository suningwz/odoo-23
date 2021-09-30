# -*- coding: utf-8 -*-
{
    'name': "safety_building",

    'summary': """
        Organise and report audits.""",

    'description': """
        Initially developped for building audit visits.
    """,

    'author': "mgaillard@vertical-access.ch",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '14.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/safety_site_views.xml',
        'views/safety_config_views.xml',
        'views/safety_audit_views.xml',
        #'views/templates.xml',
    ],

}
