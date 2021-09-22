# -*- coding: utf-8 -*-
{
    'name': "va_sales",

    'summary': """
        Vertical-Access Sales customs""",

    'description': """
        Vertical-Access Sales customs
    """,

    'author': "Vertical Access Sàrl",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Vertical-Access',
    'version': '14.0.6',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'sale_management',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        
    ],
   
}
