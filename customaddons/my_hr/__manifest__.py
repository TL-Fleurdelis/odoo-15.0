{
    'name': "Employee Management",
    'name_vi_VN': "Quản lý nhân viên",

    'summary': """
    Employee Management Demo
""",
    'summary_vi_VN': """
Quản lý nhân viên Demo 
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
    
    'data': [
        'security/security.xml',
        'data/data.xml',
        'demo/demo.xml',
        'views/views.xml',
        'views/employee_views.xml',
        'views/contract_views.xml',
        'views/relative_views.xml',
        'views/department_views.xml',
        'views/job_views.xml',
        'views/experience_views.xml',
        #'views/manager_views.xml',
        'views/templates.xml',
        'wizard/employee_wizard.xml',
        'security/ir.model.access.csv',
    ],
    'demo':[
         'demo/demo.xml',
    ],
    # only loaded in demonstration mode

    'images' : [
         'static/src/img/index.png',
         'static/description/icon.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
