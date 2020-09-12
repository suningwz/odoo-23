# -*- coding: utf-8 -*-
{
    'name': "va_sales",

    'summary': """
        Vertical-Access Sales customs""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Vertical Access",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        
    ],
   
}
