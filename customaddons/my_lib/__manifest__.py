{
    'name': "Library Management",
    'name_vi_VN': "Quản lý Thư viện",

    'summary': """
    Library Management Demo
""",
    'summary_vi_VN': """
Quản lý thư viện Demo 
""",

    'description': """


""",

    'author': "TL-Fleurdelis",
    'website': "https://github.com/TL-Fleurdelis",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'category': 'Library',

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/library_book.xml',
        'views/library_book_categ.xml',
        'views/library_book_rent.xml',
        'views/res_config_settings.xml',
        'views/views.xml',
        'data/data.xml',
        'wizard/book_rent_wizard.xml',
        'wizard/library_return_wizard.xml',
    ],
    'demo':[
         'demo/demo.xml',
    ],
    #'pre_init_hook':'init_hook',
    'post_init_hook': 'add_book_hook',
    #'post_load': 'load_book_hook',
    # only loaded in demonstration mode

    'images' : [
         #'static/src/img/index.png',
         #'static/description/icon.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
