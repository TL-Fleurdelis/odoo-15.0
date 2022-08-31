{
    'name': "Advanced Sale Management",
    'summary': """
    Advance Sales
""",
    'summary_vi_VN': """
Bán hàng nâng cao  
""",

    'description': """


""",
    'author': "TL-Fleurdelis",
    'website': "https://github.com/TL-Fleurdelis",
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'l10n_de'],
    # always loaded
    'data': [
        'security/new_customer_security.xml',
        'views/new_sale_order_views.xml',
        'views/new_customer_views.xml',
        'views/new_menu_views.xml',
        'wizard/customer_wizard_views.xml',
        'security/ir.model.access.csv',
        #'views/templates.xml',
    ],

}
