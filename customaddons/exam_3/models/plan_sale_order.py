from odoo import models, fields
from odoo.exceptions import UserError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread']

    name = fields.Text(required=True, tracking=True)
    quotation = fields.Many2one('sale.order', store=True)
    content = fields.Text(string='Content of the quotations', required=True, tracking=True)

    state = fields.Selection([
        ('unknown', 'Unknown'),
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State of quotation', readonly=True, tracking=True, default='unknown')

    order_line = fields.One2many('plan.sale.order.list', 'order_id', string='Order Lines',
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                 copy=True, tracking=True)
    can_confirm = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', tracking=True)

    # Button set up new plan
    def btn_new(self):
        self.state = 'new'
        self.order_line.approval_status = 'unavailable'
        self.can_confirm = 'no'

    # Button send plan for supreme approver
    def btn_send(self):

        mess_send = 'The new plan has been sent to the person in charge by email on %s . Created by %s.' \
                    % (fields.Datetime.now(), self.create_uid.name)

        if self.state == 'new':
            if self.order_line.approver:
                self.state = 'send'
                self.message_post(subject='Send to Approver', body=mess_send, message_type='notification',
                                  partner_ids=self.order_line.approver.ids)
            else:
                raise UserError('This plan does not have any approvers.')
        else:
            raise UserError('Cannot send this approver.'
                            ' Maybe you sent gmail before. Please press New button to create a new plan and try again.')

    # Button confirm approve (for supreme approver)
    def btn_confirm_approve(self):

        mess_approve = "The new plan of %s has been approved on %s" % (self.create_uid.name, fields.Datetime.now())

        if self.can_confirm == 'yes':
            if self.order_line.approver:
                self.state = 'approve'
                self.message_post(subject='Approve New Plan', body=mess_approve)
            else:
                raise UserError('Please write your approvers.')
        else:
            raise UserError('Cannot confirm this approve. Please check your data.')

    # Button confirm refuse (for supreme approver)
    def btn_confirm_refuse(self):

        mess_refuse = "The new plan of %s has been refused on %s" % (self.create_uid.name, fields.Datetime.now())

        if self.can_confirm == 'no':
            self.state = 'refuse'
            self.message_post(subject='Refuse New Plan', body=mess_refuse)
        else:
            raise UserError('Cannot confirm this approve. Please check your data.')
