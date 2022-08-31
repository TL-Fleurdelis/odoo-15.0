from odoo import models, fields, api
from odoo.exceptions import UserError


class CustomerWizard(models.Model):
    
    _name = 'customer.wizard'
    _description = 'Customers Wizard'

    customer_id = fields.Many2many('res.partner', string='Customers')
    wiz_customer_discount_code = fields.Text(string='Customer discount code')
    wiz_active_discount_code = fields.Boolean(string='Active discount code', default=False)
    wiz_code_value = fields.Float(compute='_compute_number_value')

    # Process the discount code string and get the value of the code
    @api.depends('wiz_active_discount_code', 'wiz_customer_discount_code')
    def _compute_number_value(self):

        for r in self:
            r.wiz_code_value = 0
            if r.wiz_customer_discount_code:
                take_code_value = self.wiz_customer_discount_code.split('_')
                show_code_value = take_code_value[-1]
                if take_code_value[0] == 'VIP' and int(show_code_value) > 0:
                    if int(show_code_value) < 100:
                        r.wiz_active_discount_code = True
                        r.wiz_code_value = int(show_code_value)
                    if int(show_code_value) >= 100:
                        r.wiz_active_discount_code = True
                        r.wiz_code_value = 100
                else:
                    r.wiz_active_discount_code = False
                    r.wiz_code_value = None
                    raise UserError('Wrong discount code !!!')

    # Active Wizard
    def set_discount_for_customers(self):

        self.ensure_one()
        self.customer_id.write({
            'customer_discount_code': self.wiz_customer_discount_code,
            'active_discount_code': self.wiz_active_discount_code,
            'code_value': self.wiz_code_value,
        })
