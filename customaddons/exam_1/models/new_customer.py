from odoo import models, fields, api


class NewCustomer(models.Model):
    _inherit = 'res.partner'

    customer_discount_code = fields.Text(string='Customer discount code', store=True)
    active_discount_code = fields.Boolean(string='Active Discount', required=False, default=False)
    code_value = fields.Float(compute='_compute_number_value')

    # Insert value of Discount Code to print Discount Code
    @api.depends('active_discount_code', 'customer_discount_code')
    def _compute_discount_value(self):
        code = 'VIP_'
        for r in self:
            if r.active_discount_code:
                r.customer_discount_code = code + str(r.numb_value)
            else:
                r.customer_discount_code = ''

    # Process the discount code string and get the value of the code
    @api.depends('active_discount_code', 'customer_discount_code')
    def _compute_number_value(self):
        for r in self:
            r.code_value = 0
            if r.customer_discount_code != '':

                take_code_value = str(r.customer_discount_code).split('_')
                show_code_value = take_code_value[-1]

                if take_code_value[0] == 'VIP' and int(show_code_value) > 0:
                    if int(show_code_value) < 100:
                        r.active_discount_code = True
                        r.code_value = int(show_code_value)
                    else:
                        r.active_discount_code = True
                        r.code_value = 100
                else:
                    r.active_discount_code = False
                    r.code_value = 0
