from odoo import models,fields

class LibraryBookRentStatistics(models.Model):

    _name = 'library.book.rent.statistics'
    _auto = False

    book_id = fields.Many2one('library.book', string='Book', readonly=True)
    rent_count = fields.Integer(string="Time borrowed",readonly=True)
    average_occupation = fields.Integer(string="Average Occupation(DAYS)", readonly=True)

