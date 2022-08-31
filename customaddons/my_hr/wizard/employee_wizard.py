from odoo import models,fields

class EmployeeWirard(models.TransientModel):
    _name = 'my.hr.employee.wizard'
    _description ='Employee Wizard Class'
    
    person_ids = fields.Many2many('my.hr.employee', string='Person')

    def make_multi_empl_to_senior(self):
        per = self.env['my.hr.employee']
        pers = per.search([('id', 'in', self.person_ids.ids)])
        for x in pers:
            x.make_senior(x)