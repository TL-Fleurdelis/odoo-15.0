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
    'depends': ['base','my_lib'],

    # always loaded

    'data': [
        'data/data.xml',
        'views/library_book_return.xml'
        #'views/library_book_categ_return.xml',
        #'views/views_return.xml'
    ],
    'demo': [
         #'demo/demo.xml',
    ],
    # only loaded in demonstration mode

    'images': [
        # 'static/src/img/index.png',
        # 'static/description/icon.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
