from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductWarranty (models.Model):
    # Inherit from  product.template
    _inherit = 'product.template'

    date_from = fields.Date(string='Date from', default=fields.Date.today)
    date_to = fields.Date(string='Date to')

    product_warranty = fields.Text(string='Product Warranty')
    sale_order_discount_estimated = fields.Float()
    calculated_discount_total = fields.Float()
    days_left = fields.Integer(string='Remaining days of warranty', compute='_compute_date', store=True)
    status_warranty = fields.Text(string='Status Warranty', compute='_compute_warranty_left')
    product_discount = fields.Float(string='Product discount (%)')

    # Sync Magento
    sync_magento = fields.Boolean()

    # Select and Unselect Magento field
    def select_sync_magento(self):
        self.sync_magento = True

    def unselect_sync_magento(self):
        self.sync_magento = False

    '''
    # Filtered để lọc các bản ghi
    
    @api.constrains('date_from','date_to')
    def check_available(self):
         if self.filtered(lambda r: r.date_from > r.date_to):
             raise ValidationError('Date from field must be sooner than Date to field')
    '''

    @api.constrains('date_from', 'date_to')
    def _check_available(self):
        for r in self:
            if r.date_from and r.date_to:
                if r.date_from > r.date_to:
                    raise ValidationError('[Date from] field must be sooner than [Date to] field')

    @api.depends('date_from', 'date_to')
    def _compute_date(self):
        for r in self:
            if r.date_from and r.date_to:
                count_date = int((r.date_to - fields.Date.today()).days)
                # print(type(days_left))
                r.days_left = count_date
            else:
                r.days_left = False

    @api.onchange('product_warranty', 'days_left')
    def _onchange_product_discount(self):
        if self.product_warranty != '':
            self.product_discount = 0
            if self.days_left < 0:
                self.product_discount = 10
        else:
            self.product_discount = 10

    # @api.depends('days_left')
    # def _compute_check_status(self):
    #     for r in self:
    #         if r.days_left == 30 or r.days_left == 31:
    #             r.status_warranty = '1 month'
    #         elif r.days_left == 60 or r.days_left == 61:
    #             r.status_warranty = '2 months'
    #         elif r.days_left == 365:
    #             r.status_warranty = '1 year'
    #         elif r.days_left == 730:
    #             r.status_warranty = '2 year'
    #         elif r.days_left <= 0:
    #             r.status_warranty = 'Out of warranty'
    #         elif r.days_left == 1:
    #             r.status_warranty = '1 day left'
    #         else:
    #             r.status_warranty = 'Still Available'

    @api.depends('date_to')
    def _compute_warranty_left(self):
        for r in self:
            if r.date_to:

                today = fields.Date.today()
                deadline_date = fields.Datetime.to_datetime(r.date_to).date()
                left_days = deadline_date - today

                years = ((left_days.total_seconds()) / (365.242*24*3600))
                years_to_int = int(years)

                months = (years - years_to_int) * 12
                months_to_int = int(months)

                days = (months - months_to_int) * (365.242 / 12)
                days_to_int = int(days)

                r.status_warranty = '{0:d} years ,' '{1:d} months ,' '{2:d}  days '\
                    .format(years_to_int, months_to_int, days_to_int)
                if years_to_int < 0 or months_to_int < 0 or days_to_int < 0:
                    r.status_warranty = 'Out of Warranty'
                else:
                    pass
            else:
                r.status_warranty = 'No warranty'

    @api.onchange('date_from', 'date_to')
    def _onchange_code_warranty(self):
        if self.date_from and self.date_to:
            str_from, str_to = str(self.date_from), str(self.date_to)

            # str_day_from, str_month_from, str_year_from = \
            #     str(self.date_from.day), str(self.date_from.month), str(self.date_from.year)[2:]
            #
            # str_day_to, str_month_to, str_year_to =\
            #     str(self.date_to.day), str(self.date_to.month), str(self.date_to.year)[2:]

            # code = 'PWD'+'/'+ str_from +'/'+ str_to

            label_day_from = str_from[8:10] + str_from[5:7] + str_from[2:4]
            label_day_to = str_to[8:10] + str_to[5:7] + str_to[2:4]
            code = 'PWD' + '/' + label_day_from + '/' + label_day_to

            self.product_warranty = code
        else:
            self.product_warranty = ''

    @api.depends('date_from', 'date_to')
    def _compute_code_warranty(self):

        for r in self:
            if r.date_from and r.date_to:
                str_from = str(r.date_from)
                str_to = str(r.date_to)

                # str_day_from, str_month_from, str_year_from = \
                #     str(r.date_from.day), str(r.date_from.month) + str(r.date_from.year)[2:]
                #
                # str_day_to, str_month_to, str_year_to = \
                #     str(r.date_to.day),str(r.date_to.month),str(r.date_to.year)[2:]

                label_day_from = str_from[8:10] + str_from[5:7] + str_from[2:4]
                label_day_to = str_to[8:10] + str_to[5:7] + str_to[2:4]

                code = 'PWD'+'/' + label_day_from + '/ ' + label_day_to
                # code2 = 'PWD'+'/' + str_from + '/' + str_to

                r.product_warranty = code
            else:
                r.product_warranty = ''
