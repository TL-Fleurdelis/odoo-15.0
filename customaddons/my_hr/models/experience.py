from odoo import models,fields, api
from odoo.exceptions import ValidationError

class Experience(models.Model):
    _name = 'my.hr.experience'
    _description = 'Experience Class'
    
    name = fields.Char(string = 'Name of job', required = True)
    company = fields.Text(string = 'Company', required = True)
    day_start = fields.Date(string = 'Start', required = True)
    day_end = fields.Date(string = 'End', required = True)
    total_exp = fields.Integer(string ='Years of experience', compute='_compute_exp')
    describe = fields.Html(string="Describe")
    
    employee_id = fields.Many2one('my.hr.employee',string='Employee ID')
    
    @api.constrains('day_start', 'day_end')
    def _check_date(self):
        if self.filtered(lambda r: r.day_start > r.day_end):
            raise ValidationError('Day start must be later than duration')
    
    @api.depends('day_start','day_end')
    def _compute_exp (self):
        for r in self:
            if r.day_start and r.day_end:
                temp = r.day_end.year-r.day_start.year
                r.total_exp = temp
            else:
                r.total_exp = 0