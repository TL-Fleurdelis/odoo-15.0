from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model): 
    _name = 'my.hr.contract'
    _description = 'Contract Class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    code = fields.Char(string='Contract code', default='New')
    name = fields.Char(string="Contract's name", required=True, tracking=True)
    day_sign = fields.Date(string='Day sign', default=fields.Date.today, tracking=True)
    duration = fields.Date(string='Duration', required=True, tracking=True)
    day_left = fields.Integer(string='Days left', compute='_compute_day_left', tracking=True)

    due = fields.Boolean(string="Status", compute='_compute_due', store=True, search='_search_due', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('expire', 'Expire'),
        ('cancel', 'Cancel')
        ], string='States', readonly=True, default='draft', tracking=True)
    # ,groups='my_hr.group_manager'
    employee_id = fields.Many2one('my.hr.employee', string='Employee ID', tracking=True) 
    
    job_id = fields.Many2one('my.hr.job', string='Job ID', domain="[('department_id', '=?', department_id)]", tracking=True)
    
    department_id = fields.Many2one('my.hr.department', string="Department", tracking=True)
    # tiền tệ
    currency_id = fields.Many2one('res.currency', string="Currency", tracking=True)
    
    price = fields.Monetary(string="Price", tracking=True)

    @api.constrains('day_sign', 'duration')
    def _check_date(self):
        # filtered sẽ trả về tập hợp các bản ghi thỏa mãn điều kiện đã cho trên một tập bản ghi hiện có
        # filtered tối ưu,làm đơn giản code, tránh điều kiệu lặp không mong muốn để đạt được điều kiện

        # lambda là hàm ẩn danh trong python => ngắn gọn, tối ưu code,thường dùng để sử dụng logic trong một chỗ nhất định trong 1 khoảng thời gian ngắn
        # lambda sẽ khó cho việc debug và bảo trì
        if self.filtered(lambda r: r.day_sign > r.duration):
            raise ValidationError('Day sign must be later than duration')
    
    '''
        compute tác dụng từ view khác
        onchange : tác dụng trên các view của hiện tại
        python constrain : chặn code python, sử dụng trong trường hợp chặn điều kiện phức tạp 
        sql constrain : ràng buộc đơn giản , tùy biến
    '''

    def _search_due(self, operator, value):
        return [('due', operator, value)]
    
    @api.depends('duration')
    def _compute_day_left(self):
        for r in self:
            if r.duration:
                temp = (r.duration - fields.Date.today()).days
                # r.day_left =(int((r.duration - fields.Date.today()).days)) # chuyển từ timedelta  -> days
                r.day_left = int(temp)
            else:
                r.day_left = False
                
    @api.depends('day_left')
    def _compute_due(self):
        for r in self:
            if r.day_left > 0:
                r.due = True
            else:
                r.due = False

    '''
    @api.model        
    def create(self, vals):
        res = super(Contract, self).create(vals)
        for r in res:
            r.name = r.name.capitalize() # string name type person
        return res
    '''
    #Capitalize contract's name (In hoa ký tự đầu tiên trong tên hợp đồng)
    '''
    @api.model
    def create(self, vals):
       
        if vals.get('name'):
            vals["name"] = vals["name"].capitalize()
        return super(Contract, self).create(vals)
    '''
    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = 'New Contract'
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('my.hr.contract') or ('New')
        if vals.get('name'):
            vals["name"] = vals["name"].capitalize()
        res = super(Contract, self).create(vals)
        
        return res

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].capitalize()
        res = super(Contract, self).write(vals)
        return res
    
    def unlink(self):
        print('Call unlink')
        for r in self:
            if r.state == 'approve':
                raise ValidationError("You cannot delete this contract because this contract is still in approve. Just delele when this contract is not approve and expire.")
        return super(Contract, self).unlink()
    
    #Sự kiện cho button
    def action_approve(self):
        print('click button approve')
        self.state = 'approve'
    
    def action_draft(self):
        print('click button draft')
        self.state = 'draft'

    def action_cancel(self):
        print('click button Cancel')
        self.state = 'cancel'
    
    def action_expire(self):
        print('click button Expire')
        self.state = 'expire'