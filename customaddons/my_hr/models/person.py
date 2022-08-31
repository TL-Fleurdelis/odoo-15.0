from odoo import models, fields, api
import re
from odoo.exceptions import UserError

class Person(models.Model):
    _name = 'my.hr.person'
    _description = 'Person Class'
    _inherit=['mail.thread','mail.activity.mixin']
    name = fields.Char(string='Full name', required=True, tracking=True)
    
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')],
                            string='Sex',
                            default='male',
                            required=True,
                            tracking=True,
                            help="Giới tính")
    
    birthday = fields.Date(string="Birthday", tracking=True)
    age = fields.Char(string = "Age", compute = '_compute_age',tracking=True)
    address = fields.Text(string='Address',required=True, tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True) 
    phone = fields.Char(string='Phone', required=True, tracking=True)
    
    #compute
    @api.depends('birthday')
    def _compute_age(self):
        for r in self:
            current_year = fields.Date.today().year
            if r.birthday:
                temp = current_year - r.birthday.year
                r.age = int(temp)   
            else:
                r.age = 0

    #compute: chỉ tính toán nhưng không lưu dữ liệu sau khi tính toán
    #onchange : dữ liệu sau khi tính toán lưu vào database
    
    @api.constrains('email')
    def validate_mail(self):
        if self.email:
            check = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
        if not check:
            raise UserError(('Wrong E-mail type'))
        
    @api.constrains('phone')
    def validate_mobile(self):
        if self.phone:
            check = re.match('^[0-9]\d{9}$', self.phone)
        if not check:
            raise UserError(('Wrong phone type'))
    
    @api.onchange('birthday')
    def _onchange_age(self):
        for r in self:
            current_year = fields.Date.today().year
            if r.birthday:
                temp = current_year - r.birthday.year
                r.age = int(temp)   
            else:
                r.age = 0     
                 
    '''           
    @api.model        
    def create(self, vals):
        res = super(Person, self).create(vals)
        print("Self in create:",self)
        print("Vals in create:",vals)
        for r in res:
            r.name = r.name.title() # string name type person
        print("Res in create:",res)
        return res
    ''' 
                
    @api.model
    def create(self, vals):
        if vals.get('name'):    
            vals["name"] = vals["name"].title()
        return super(Person, self).create(vals)
    
    def write(self,vals):
        print("Self in write",self)
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        res = super(Person,self).write(vals)
        return res
    