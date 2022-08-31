from odoo import models, fields


class WarrantyWizard(models.Model):
    _name = 'warranty.wizard'
    _description = 'Warranty Wizard'
    product_id = fields.Many2many('product.template', string='Product')
    wiz_date_from = fields.Date()
    wiz_date_to = fields.Date()

    def set_warranty_for_product(self):
        self.ensure_one()
        self.product_id.write({

            'date_from': self.wiz_date_from,
            'date_to': self.wiz_date_to,

        })
