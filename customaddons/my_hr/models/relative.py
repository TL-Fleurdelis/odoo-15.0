from odoo import models, fields

class Relative(models.Model):
    _name = 'my.hr.relative'
    _description = 'Relative Class'
    
    _inherit = 'my.hr.person'
    '''
    name    = fields.Char(string ='Name',required = True)
    address = fields.Text (string='Address', required=True)
    email   = fields.Char (string='Email', required=True) 
    phone   = fields.Char (string='Phone', required=True)
    '''
    #ondelete = "cascade"
    # nếu xóa nhân viên này, ngay lập tức sẽ xóa tất cả thông tin người thân liên quan 
    employee_id = fields.Many2one ('my.hr.employee', string = "Employee",ondelete='cascade')
    #ondelete có 3 loại
    #cascade: xóa thông tin liên quan, set null: thiết lập trường liên kết về null , restrict: Không cho xóa