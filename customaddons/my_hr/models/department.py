from odoo import models, fields, api

class Department(models.Model):
    _name = 'my.hr.department'
    _description = 'Department Class'
    
    name = fields.Char(string='Name of Department', required=True)
    room = fields.Char(string='Room' , required=True)
    phone = fields.Char(string="Phone's number", required=True)
    
    employee_ids = fields.One2many('my.hr.employee','department_id',string='Employee ID')

    job_ids = fields.One2many('my.hr.job','department_id', string="List job")
    
    contract_ids = fields.One2many('my.hr.contract','department_id', string='Contract')
    
    count_employees = fields.Integer(string='Number of employees',compute='_compute_employees_count',store=True)
    count_jobs = fields.Integer(string='Number of jobs',compute='_compute_jobs_count',store=True)
    
    @api.depends('employee_ids')
    def _compute_employees_count(self):
        for i in self:
            i.count_employees = len(i.employee_ids)
            
    @api.depends('job_ids')
    def _compute_jobs_count(self):
        for i in self:
            i.count_jobs = len(i.job_ids)
        
    
    '''
    @api.model
    def name_create(self,name):
        print("name_create: ", name)
        res = self.create({'name':name,'phone':'123'})
        return res.name.get()[0]
    '''