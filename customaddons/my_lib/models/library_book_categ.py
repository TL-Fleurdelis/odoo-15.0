from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BookCategory(models.Model):
    _name = 'library.book.category'
    _description ="Book Category"
    name = fields.Char('Category',required=True)
    parent_id = fields.Many2one('library.book.category',string='Parent Category',ondelete='restrict', index=True)
    #index: tăng tốc hiệu suất tìm kiếm cơ sở dữ liệu, tuy nhiên k nên thêm index quá nhiều vì có thể làm tăng kích thước CSDL
    book_ids = fields.One2many('library.book','category_id',string ="Book id")
    child_ids = fields.One2many('library.book.category', 'parent_id', string='Child Categories')
    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'
    parent_path = fields.Char(index=True)
    email = fields.Char(string="Email")
    description = fields.Text('Description')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError('Error! You cannot create recursive categories.')

    # category_id = fields.Many2one('library.book.category',string="Category_id")

    def create_categ(self):
        categ1 ={'name':'Child categ 1',
                 'description':'Description for child 1'
                }
        categ2 ={'name':'Child categ 2',
                 'description':'Description for child 2'
                }
        parent_category_val = {
            'name': 'Parent category',
            'email': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        record = self.env['library.book.category'].create(parent_category_val)
        print(record)
        categ3 = {
            'name': 'Category 1',
            'description': 'Description for Category 1'
        }
        categ4 = {
            'name': 'Category 2',
            'description': 'Description for Category 2'
        }
        multiple_records = self.env['library.book.category'].create([categ3, categ4])
        print(multiple_records)