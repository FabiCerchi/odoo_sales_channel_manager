# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    sale_channel_id = fields.Many2one('sales.channel', string = 'Canal de venta', required = True)
    #Override field
    warehouse_id = fields.Many2one(compute="_compute_warehouse_id")
    credit_status = fields.Selection([('no_limit', 'Sin limite de credito'),
                                ('with_credit', 'Credito disponible'),
                                ('blocked_credit', 'Credito bloqueado')],
                                string='Credito',
                                default='no_limit',
                                compute='_compute_credit_status',
                                store=True,
                                readonly=True)
    
    @api.depends('sale_channel_id')
    def _compute_warehouse_id(self):
        for rec in self:
            rec.warehouse_id = rec.sale_channel_id.warehouse_id
    
    @api.depends('partner_id', 'amount_total')
    def _compute_credit_status(self):
        for rec in self:
            credit_group_id = self.env['sales.credit.group'].search([('sale_channel_id','=', rec.sale_channel_id.id),('partner_ids','in',rec.partner_id.id)], limit=1)
            if not credit_group_id:
                rec.credit_status = 'no_limit'
            else:
                if rec.amount_total > credit_group_id.avaiable_credit:
                    rec.credit_status = 'blocked_credit'
                else:
                    rec.credit_status = 'with_credit'
            
    #Override
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
        invoice_vals['journal_id'] = self.sale_channel_id.journal_id.id
        invoice_vals['sale_channel_id'] = self.sale_channel_id.id
        return invoice_vals

    #Override
    def action_confirm(self):
        for rec in self:
            if rec.credit_status == 'blocked_credit':
                raise ValidationError('No se puede confirmar la venta, el credito esta bloqueado')
        order = super(SaleOrderInherit, self).action_confirm()
        return order
