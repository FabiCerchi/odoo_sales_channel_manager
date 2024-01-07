# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'
    
    sale_channel_id = fields.Many2one('sales.channel', related="sale_id.sale_channel_id", store = True)