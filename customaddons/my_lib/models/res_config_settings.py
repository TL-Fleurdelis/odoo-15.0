from odoo import models,fields,api

class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    group_release_dates = fields.Boolean('Manage book release dates',
                                         group='base.group_user',
                                         implied_group='my_lib.group_release_dates')
    module_note = fields.Boolean('Install Notes App')