# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    sale_channel_id = fields.Many2one('sales.channel', string= 'Canal de Venta', readonly=True)  