from odoo import models, fields
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    plan_sale_order = fields.Many2one('plan.sale.order', string='Plan sale order')
    # ondelete='cascade',index=True, copy=False, invisible=True

    plan_sale_order_id = fields.One2many('plan.sale.order', 'quotation', string='Order')
    new_quotation = fields.Many2one(related='plan_sale_order_id.quotation')
    new_state = fields.Selection(related='plan_sale_order_id.state')

    def _action_confirm(self):
        for order in self:
            if any(expense_policy not in [False, 'no'] for expense_policy in
                   order.order_line.mapped('product_id.expense_policy')):
                if not order.analytic_account_id:
                    order._create_analytic_account()
        return True

    def action_done(self):
        for order in self:
            tx = order.sudo().transaction_ids._get_last()
            if tx and tx.state == 'pending' and tx.acquirer_id.provider == 'transfer':
                tx._set_done()
                tx.write({'is_post_processed': True})
        return self.write({'state': 'done'})

    def _prepare_confirmation_values(self):
        return {
            'state': 'sale',
            'date_order': fields.Datetime.now()
        }

    def _get_forbidden_state_confirm(self):
        return {'done', 'cancel'}

    # Confirm button in Sale orders
    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))
        if not self.new_quotation or self.new_state != 'approve':
            raise models.ValidationError('Not available/Not approved plan sale order')
        # Source from Sale Order
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())
        context = self._context.copy()
        context.pop('default_name', None)
        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True
