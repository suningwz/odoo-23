# -*- coding: utf-8 -*-
{
    'name': "va_admin",

    'summary': """
        vertical-access.ch Admin Module""",

    'description': """
        Used to install root data and custom Vertical-Access Modules
    """,

    'author': "Vertical Access Sàrl",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Vertical-Access',
    'version': '14.0.7',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        ],

    # always loaded
    'data': [
        'data/res_company.xml',
        'views/colors.xml',
    ],

}
