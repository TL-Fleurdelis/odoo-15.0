{
    'name': "Product Management",
    'name_vi_VN': "Quản lý Sản phẩm",

    'summary': """

""",
    'summary_vi_VN': """

""",

    'description': """


""",

    'author': "TL-Fleurdelis",
    'website': "https://github.com/TL-Fleurdelis",


    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_management', 'exam_1', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_warranty.xml',
        'views/new_menu_views.xml',
        'wizard/warranty_wizard_views.xml',
        #'views/templates.xml',
    ],

}
