from . import models
from . import wizard
from . import controllers
from odoo import api, fields, SUPERUSER_ID
def add_book_hook(cr,registry):
    env = api.Environment(cr, SUPERUSER_ID,{})
    book_data1 = {'name':'Book 1','date_release': fields.Date.today(),'short_name':'B1'}
    book_data2 = {'name':'Book 2','date_release': fields.Date.today(),'short_name':'B2'}
    env['library.book'].create([book_data1, book_data2])
# def init_hook(cr):
#     env = api.Environment(cr, SUPERUSER_ID,{})
#     book_data3 = {'name':'Book 3','date_release': fields.Date.today(),'short_name':'B3'}
#     book_data4 = {'name':'Book 4','date_release': fields.Date.today(),'short_name':'B4'}
#     env['library.book'].create([book_data3, book_data4])

# def load_book_hook(cr,registry):
#     env = api.Environment(cr, SUPERUSER_ID,{})
#     book_data3 = {'name':'Book 3','date_release': fields.Date.today(),'short_name':'B3'}
#     book_data4 = {'name':'Book 4','date_release': fields.Date.today(),'short_name':'B4'}
#     env['library.book'].create([book_data3, book_data4])