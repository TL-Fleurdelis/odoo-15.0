import  base64
from odoo.exceptions import ValidationError
from odoo import models, fields, api
from odoo.modules.module import get_module_resource

class Employee(models.Model):
    _name = 'my.hr.employee'
    _description = 'Employee Class'
    _inherit = ['my.hr.person','mail.thread','mail.activity.mixin']
    
    '''
    name = fields.Char (string = "Name", required=True)
    birthday = fields.Date(string = "Birthday")
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Sex', default='male', required=True, help = "This is your gender")
    address = fields.Text (string='Address', required=True)
    email = fields.Char (string='Email', required=True) 
    phone = fields.Char(string='Phone', required=True)
    '''
    
    def _default_image(self):
        #self.ensure_one() # kiểm tra đây là 1 bản ghi duy nhất
        image_path = get_module_resource('my_hr', 'static/src/img', 'index.png')
        return base64.b64encode(open(image_path, 'rb').read())
    img = fields.Binary(string="Upload image", default= _default_image, attachment = True)
    #img = fields.Image(string="Upload image", default= _default_image, attachment = True)
    department_id = fields.Many2one ('my.hr.department', string = 'Department',ondelete='restrict')
    contract_ids  = fields.One2many ('my.hr.contract', 'employee_id', string = 'Contract ID', readonly=True)
    identity_card = fields.Char("Identity card", required = True)

    relative_ids  = fields.One2many('my.hr.relative', 'employee_id', string = 'Relative ID', readonly=True)
    job_id = fields.Many2one('my.hr.job', string='Job ID', domain="[('department_id', '=?', department_id)]",ondelete='restrict')
    level = fields.Char(string ='Level')    

    education = fields.Selection([('university','University'),
                                ('college','College'),
                                ('another','Another')],
                                string = "Education",default='university')
    school = fields.Char(string='School',default='Unknown')
    gpa = fields.Float(string = "GPA")
    experience_ids = fields.One2many('my.hr.experience','employee_id', string ="Experience ID", readonly=True)
    
    #_sql_constraints = [('identity_card_unique', 'unique(identity_card)', "This ID card number may be the same as someone else")]
   
    @api.constrains('identity_card')
    def check_id(self):
        self.ensure_one()
        if self.identity_card:    
            if self.env['my.hr.employee'].search_count([('identity_card','=',self.identity_card)]) > 1:
                raise ValidationError('API This ID card number may be the same as someone else')
         
    def make_senior(self, empl):    
        empl.write({'level': 'senior'})
        
    
    def test_recordset(self):
        print('test self:', self[0].name)
        for rec in self:
            print("test recordset")
            employees = self.env['my.hr.employee'].search([])
            
            print('Mapped: ', employees.mapped('name'))
            print('Sorted:', employees.sorted(lambda temp:temp.write_date)) # tăng dần theo khoảng thời gian
            print('Sorted reverse: ', employees.sorted(lambda temp:temp.write_date, reverse = True)) # đảo lại thứ tự
            print('Filter employee who not in any department: ',employees.filtered(lambda temp:not temp.department_id)) # lọc ra nhân viên chưa ở 1 phòng ban nào 
            print('Filter following domain',employees.filtered_domain([('sex', '=', 'male')]))
            print('Read group: ',employees.read_group([],fields=['department_id'],groupby='department_id'))
            print('Read group sex: ',employees.read_group([],fields=['name'],groupby='sex'))
            print('Field get all: ',employees.fields_get())
            # fields_get trả về cả các trường kế thừa
            #print('Field get all: ',employees.fields_get(['name','department_id']))
            print('Field get name: ',employees.fields_get(['name'],['type','string']))
        return rec

    #Override copy method 
    def copy(self,default = {}):
        
        default['identity_card'] = 'Identity clone'
        default['name'] = 'Clone of ' + self.name
        
        clone = super(Employee, self).copy(default)
        print("Copy method: ",clone)
        
        return clone
    '''
    def name_get(self):
        result = []
        for r in self:
            name = r.name
            result.append(r.id,name)
            
    def name_create(self,name):
        
        #print("name_create: ", name)
        
        res = self.create({'name':'abc','email':'abc@gmail'})
        return res.name.get()[0]
        
        return self.create({'name':name}).name_get()[0]
        
    '''
    # Set default field
    @api.model 
    def default_get(self,field_list=[]):
        
        print("field list",field_list)
        res = super(Employee,self).default_get(field_list)
        print("before edit: ",res)
        res['name'] = 'pitaya'
        res['email'] ='p@gmail.com'
        res['phone'] = '1111111111'
        res['address'] = "Default Hải Phòng"
        print('after edit default:',res) 
        return res

    def search_employee_male(self):
        search_employee = self.env['my.hr.employee'].search([('sex','=','male')])
        print('Male:',search_employee)
        count = self.env['my.hr.employee'].search_count([('sex','=','male')])
        print("Male's number: ", count)
    
    def search_employee_female(self):
        search_employee = self.env['my.hr.employee'].search([('sex','=','female')])
        print('Female:',search_employee)
        count = self.env['my.hr.employee'].search_count([('sex','=','female')])
        print("Female's number: ", count)      
        
    def temp (self):
        new_employee = self.env['my.hr.employee'].create([{'name':'long','identity_card': '1092','phone':'1111111111','email':'a@gmail.com','address':'abc'}])
        print('Here:', new_employee)    
    '''
    @api.model
    def create(self, vals):
        if vals.get('name'):    
            vals["name"] = vals["name"].title()
        return super(Employee, self).create(vals)
    
    def write(self,vals):
        print("Self in write",self)
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        res = super(Employee,self).write(vals)
        return res
    '''
    '''
    #overide write. If change something in record  =>  change vals
    def write(self,vals):
        print("Values: ",vals)
        vals['school']='ZERO'
        vals['gpa']= 3.05
        res = super(Employee,self).write(vals)
        return res
        #print("Write method:",res) #res = true
    '''