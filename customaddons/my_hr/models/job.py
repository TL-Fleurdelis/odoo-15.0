from odoo import models, fields

class Job(models.Model):
    _name = 'my.hr.job'
    _description = "Job Class"
    name = fields.Char(string ='Name',required=True)
    job_decription = fields.Text(string = "Describe")
    department_id = fields.Many2one('my.hr.department',string = 'Department')
    employee_ids = fields.One2many('my.hr.employee','job_id',string ="Employee")
