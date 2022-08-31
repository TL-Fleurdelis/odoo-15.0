from odoo import models,fields

class Manager(models.Model):
    _name = 'my.hr.admin'
    _description = 'Admin Class'
    #_inherit=['mail.thread','mail.activity.mixin']
