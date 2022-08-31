from odoo import models,fields,api
import logging
_logger = logging.getLogger(__name__)

class LibraryBookRent(models.Model):
    _name = 'library.book.rent'

    book_id = fields.Many2one('library.book',required = True)

    borrower_id = fields.Many2one('res.partner','Borrower', required = True)
    state = fields.Selection([('ongoing','Ongoing'),
                              ('returned','Returned'),
                              ('lost','Lost')],
                              string = 'State', default='ongoing', required=True)
    rent_date = fields.Date(string='Rent date', default=fields.Date.today())
    return_date = fields.Datetime(string='Return date',readonly=True)
    '''
    def book_rent(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError('Book is not available')
        rent_as_superuser = self.env ['library.book.rent'].sudo()
        rent_as_superuser.create({
            'book_id': self.id,
            'borrower_id': self.env.user.partner_id.id
        })
    '''
    # def make_lost(self):
    #     self.ensure_one()
    #     self.state = 'lost'
    #     if not self.env.context.get('avoid_deactivate'):
    #         self.active = False

    def book_lost(self):
        self.ensure_one()
        self.sudo().state = 'lost'
        book_with_difference_context = self.book_id.with_context(avoid_deactivate=True)
        book_with_difference_context.sudo().make_lost()

    def book_return(self):
        self.ensure_one()
        self.sudo().state = 'returned'
        self.sudo().return_date = fields.Datetime.now()
        book_with_difference_context = self.book_id.with_context(avoid_deactivate=True)
        book_with_difference_context.sudo().make_available()

    @api.model
    def create(self, vals):
        book_rec = self.env['library.book'].browse(vals['book_id'])
        book_rec.make_borrowed()
        return super(LibraryBookRent, self).create(vals)

    # def book_return(self):
    #     self.ensure_one()
    #     self.book_id.make_available()
    #     self.write({
    #         'state': 'returned',
    #         'return_date': fields.Date.today()
    #     })
