# -*- coding: utf-8 -*-
{
    'name': "va_document",

    'summary': """
        Vertical-Access Documents""",

    'description': """
        Used to process CSV file for custom imports
    """,

    'author': "Vertical Access Sàrl",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Vertical-Access',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'documents',
        ],

    # always loaded
    'data': [
        'data/csv_import_data.xml'
    ],

}
