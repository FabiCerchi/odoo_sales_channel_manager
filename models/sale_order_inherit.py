# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    sale_channel_id = fields.Many2one('sales.channel', string = 'Canal de venta', required = True)
    #Override field
    warehouse_id = fields.Many2one(compute="_compute_warehouse_id")
    
    
    @api.depends('sale_channel_id')
    def _compute_warehouse_id(self):
        for rec in self:
            rec.warehouse_id = rec.sale_channel_id.warehouse_id
    
    #Override
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
        invoice_vals['journal_id'] = self.sale_channel_id.journal_id.id
        invoice_vals['sale_channel_id'] = self.sale_channel_id.id
        return invoice_vals
        
        
