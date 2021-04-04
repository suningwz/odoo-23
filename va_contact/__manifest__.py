# -*- coding: utf-8 -*-
{
    'name': "va_contact",

    'summary': """
        vertical-access.ch Contact Customs""",

    'description': """
        Host the custom modifications required for contact management for vertical access.
    """,

    'author': "Vertical Access Sàrl",
    'website': "http://www.vertical-access.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Vertical-Access',
    'version': '14.0.8',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
        'partner_firstname',
        'partner_company_group',
        'va_admin',
        ],

    # always loaded
    'data': [
        #security
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        #views
        'views/res_partner_views.xml',
        'views/social_reason_views.xml',
    ],

}
