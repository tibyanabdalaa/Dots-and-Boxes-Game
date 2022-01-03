from odoo import models, fields, api


class Configuration(models.Model):
    _name = 'config.details'
    _inherit = 'mail.thread'
    _description = 'Update App Configuration'

    name = fields.Char(default='Help Data')
    help_data = fields.Html('Help', default='', track_visibility='True')
