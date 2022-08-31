# -*- coding: utf-8 -*-
# from odoo import http


# class MyHr(http.Controller):
#     @http.route('/my_hr/my_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_hr/my_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_hr.listing', {
#             'root': '/my_hr/my_hr',
#             'objects': http.request.env['my_hr.my_hr'].search([]),
#         })

#     @http.route('/my_hr/my_hr/objects/<model("my_hr.my_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_hr.object', {
#             'object': obj
#         })
