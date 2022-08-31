import datetime
from odoo import http, fields
from odoo.http import request
import email
#from odoo.addons.website.controllers.main import Website

# class WebsiteInfo(Website):
#     @http.route()
#     def website_info(self):
#         result = super(WebsiteInfo, self).website_info()
#
#         result.qcontext['apps'] = result.qcontext['apps'].filtered(lambda x: x.name != 'website')
#         return result

class Main(http.Controller):
    @http.route('/my_lib/books', type='http',auth='none')
    def books(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s:%s Authors:%s </li>" % (book.name,book.date_release,book.author_ids)
        html_result += '</ul></body></html>'
        #return html_result
        request.session['hello'] = 'world'
        request.session.get('hello')
        return request.make_response(
            html_result, headers=[

                ('Last-modified', email.utils.formatdate((
                    fields.Datetime.from_string(
                    request.env['library.book'].sudo().search([],order='write_date desc', limit=1)
                    .date_updated) - datetime.datetime(1970, 1,1)).total_seconds(),usegmt=True))
            ])
    @http.route('/my_lib/all-books', type='http', auth='none')
    def all_books(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result +="<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/my_lib/all-books/mark-mine',type='http', auth='public')
    def all_books_mark_mine(self):
        books = request.env['library.book'].sudo().search([])

        html_result = '<html><body><ul>'
        for book in books:
            if request.env.user.partner_id.id in book.author_ids.ids:
                html_result += "<li> <b>%s</b> </li>" % book.name
            else:
                html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/my_libr/all-books/mine', type='http',auth='user')
    def all_books_mine(self):
        books = request.env['library.book'].search([
            ('author_ids', 'in', request.env.user.partner_id.ids),
        ])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result
    @http.route('/my_lib/books_details', type='http',auth='none')
    def book_details(self,book_id):
        record = request.env['library.book'].sudo().browse(int(book_id))
        return u'<html><body><h1>%s</h1>Authors:%s' %(record.name, u','.join(record.author_ids.mapped('name')) or 'none',)

    @http.route("/my_lib/books_details/<model('library.book'):book>",type='http',auth='none')
    def book_details_in_path(self, book):
        return self.book_details(book.id)

    @http.route('/my_lib/books/json', type='json', auth='none')
    def books_json(self):
        records = request.env['library.book'].sudo().search([])
        return records.read(['name'])

    @http.route('/demo_page',type='http',auth='none')
    def books(self):
        image_url = '/my_lib/static/src/image/index.png'
        html_result = """<html>
            <body>
                <img src="%s"/>
            </body>
            </html>""" % image_url
        return html_result