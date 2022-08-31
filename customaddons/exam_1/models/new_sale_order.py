from odoo import models, fields


class NewSaleOrder(models.Model):

    _inherit = 'sale.order'

    customer_discount_code = fields.Text(string='Customer discount code', related='partner_id.customer_discount_code')
    code_value = fields.Float(string='Sale order discount', related='partner_id.code_value')
    active_discount_code = fields.Boolean(related='partner_id.active_discount_code')