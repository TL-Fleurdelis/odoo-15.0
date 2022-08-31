from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
import requests
from datetime import timedelta
from odoo.tests.common import Form
import logging
_logger = logging.getLogger(__name__)


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Base Archive'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):

    _name = 'library.book'
    _inherit = ['base.archive', 'mail.thread', 'mail.activity.mixin']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    # rec name dùng để xác định giá trị bản ghi dùng để
    # hiển thị trong việc tìm kiếm các trường cho many2one và những trường hợp khác

    # hiển thị trên thanh web
    # ví dụ short_name = D, _rec_name='short_name' => hiển thị trên thanh web : Odoo-D

    name = fields.Char('Title', required=True, tracking=True)
    short_name = fields.Char('Short Title', tracking=True)
    notes = fields.Text('Internal Notes', tracking=True)
    description = fields.Html('Description', sanitize=True, strip_style=False, tracking=True)
    cover = fields.Binary('Book Cover', attachment=True, tracking=True)
    author_ids = fields.Many2many('res.partner', string='Authors', tracking=True)
    # out_of_print = fields.Boolean('Out of Print?').

    # date_release = fields.Date('Release Date',tracking=True)
    date_release = fields.Date('Release Date', groups='my_lib.group_release_dates')
    date_updated = fields.Datetime('Last Updated', tracking=True)

    pages = fields.Integer('Number of Pages',
                           groups='base.group_user',
                           states={'lost': [('readonly', True)]},
                           help='Total book page count',
                           company_dependent=False, tracking=True)

    reader_rating = fields.Float('Reader Average Rating', digits=(14, 4),  # Optional precision decimals,)
                                 )
    cost_price = fields.Float('Book Cost', digits='Book Price', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', tracking=True)
    retail_price = fields.Monetary('Retail Price', tracking=True)
    # optional: currency_field='currency_id',

    publisher_id = fields.Many2one('res.partner', string='Publisher', tracking=True)
    # optional:ondelete='set null',context={}, domain=[],
    publisher_city = fields.Char(string='Publisher City', related='publisher_id.city', readonly=True, tracking=True)
    age_days = fields.Float(string='Days Since Release', compute='_compute_age', inverse='_inverse_age',
                            search='_search_age', store=False, tracking=True)
    # optional compute_sudo=True
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)', 'No of pages must be positive')
        ]
    # ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')

    state = fields.Selection([
        ('unavailable', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        string='State', default="unavailable", readonly=True)

    category_id = fields.Many2one("library.book.category", string="Category ID")
    rent_ids = fields.One2many('library.book.rent', 'book_id', string="Book", readonly=True)

    manager_remarks = fields.Text('Manager Remarks')
    isbn = fields.Char('ISBN')

    is_public = fields.Boolean(groups='my_lib.group_library_librarian')
    private_notes = fields.Text(groups='my_lib.group_library_librarian')

    report_missing = fields.Text(string='Book is missing', groups='my_lib.group_library_librarian')

    def report_missing_book(self):
        self.ensure_one()
        message = 'Book is missing(Report by %s)' % self.env.user.name
        self.sudo().write({
            'report_missing': message
        })

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    # kiểm tra ngày cập nhật có lớn hơn ngày phát hành sách hay không
    @api.constrains('date_release', 'date_updated')
    def _check_release_update(self):
        for record in self:
            if record.date_release and record.date_updated and record.date_updated.date() < record.date_release:
                raise ValidationError('Date update < Date Release ==> Wrong')

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                age = today - book.date_release
                book.age_days = age.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()

        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d
    #
    # @api.model
    # def _referencable_models(self):
    #     return
        # models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        # return [(x.model, x.name) for x in models]

    '''
    def _search_age(self, operator, value):
        today = fields.Date.today()

        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]
    '''

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)
                raise UserError(msg)

    def post_to_webservice(self, data):
        try:
            req = requests.post('http://my-test-service.com', data=data, timeout=10)
            content = req.json()
        except IOError:
            error_msg = _("Something went wrong during data submission")
            raise UserError(error_msg)
        return content

    def change_update_date(self):
        self.ensure_one()
        self.update({'date_updated': fields.Datetime.now()})

    def find_book(self):
        domain = [
            '|',
            '&', ('name', 'ilike', 'Dark'),
            ('category_id.name', 'ilike', 'abc'),

             '&', ('name', 'ilike', 'Dark2'),
            ('category_id.name', 'ilike', 'abc')
        ]
        books = self.search(domain)
        print(books)
    '''
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed=[('draft', 'available'),
                ('available', 'borrowed'),tho
                ('borrowed', 'available'),
                ('available', 'lost'),
                ('borrowed', 'lost'),
                ('lost', 'available')]
        return (old_state, new_state) in allowed
    '''
    '''
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue
    '''
    '''
    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')
    '''

    '''
    def books_with_multiple_authors(self):
        #debug = 1
        #print(all_books.filter(lambda b: len(b.author_ids) > 1))
        # return all_books.filter(lambda b: len(b.author_ids) > 1)
        # return filter(all_books, lambda b: len(b.author_ids) > 1)
        all_books = self.search([])
        res = all_books.filtered(lambda b: len(b.author_ids) > 1)
        return res
    '''
    def make_unavailable(self):
        self.state = 'unavailable'

    def make_available(self):
        self.state = 'available'

    def make_borrowed(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError('Cannot renting')
        else:
            self.state = 'borrowed'

    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'
        # if not self.env.context.get('avoid_deactivate'):
        #     self.active = False
    '''
    @api.model
    def create(self, values):
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )
        return super(LibraryBook, self).create(values)
    '''

    def return_all_books(self):
        self.ensure_one()
        wizard = self.env['library.return.wizard']
        with Form(wizard) as return_form:
            return_form.borrower_id = self.env.user.partner_id
            record = return_form.save()
            record.books_returns()

    # def return_all_books(self):
    #     self.ensure_one()
    #     wizard = self.env['library.return.wizard']
    #     wizard.create({
    #         'borrower_id': self.env.user.partner_id.id
    #     }).books_returns()

    def write(self, values):
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )

        return super(LibraryBook, self).write(values)

    def unlink(self):
        return super(LibraryBook, self).unlink()

    def name_get(self):
        result = []

        for book in self:
            authors = book.author_ids.mapped('name')
            name = '%s (%s)' % (book.name, ', '.join(authors)) if authors else book.name
            result.append((book.id, name))
        return result

    # @api.model
    # def _name_search(self, name='', args=None,operator='ilike', limit=100, name_get_uid=None):
    #     args = [] if args is None else args.copy()
    #     if not(name == '' and operator == 'ilike'):
    #         args += ['|', '|',
    #                  ('name', operator, name),
    #                  ('isbn', operator, name),
    #                  ('author_ids.name', operator, name)
    #                  ]
    #     return super(LibraryBook, self)._name_search(name=name,
    #     args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    def average_book_occupation(self):
        self.flush()
        sql_query = """
            SELECT
                lb.name,
                avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
            FROM
                library_book_rent AS lbr
            JOIN
                library_book as lb ON lb.id = lbr.book_id
            WHERE lbr.state = 'returned'
            GROUP BY lb.name;"""
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        _logger.info("Average book occupation: %s", result)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many('library.book', string='Authored Books')
    # relation='library_book_res_partner_rel' #optional

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Members'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner', ondelete='cascade', required=True)
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')

    def log_all_library_members(self):
        # This is an empty recordset of model library.member
        library_member_model = self.env['library.member']
        all_members = library_member_model.search([])
        print("All Members:", all_members)
        return True
