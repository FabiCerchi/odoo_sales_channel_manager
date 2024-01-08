# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api
from odoo.exceptions import ValidationError

class SalesCreditGroup(models.Model):
    _name = 'sales.credit.group'
    _description = 'Gestiona los creditos para diferentes clientes'
    
    name = fields.Char(string = 'Nombre', required = True)
    code = fields.Char(string = 'Codigo', copy = False, required = True)
    sale_channel_id = fields.Many2one('sales.channel', string = 'Canal de venta', required = True)
    currency_id = fields.Many2one('res.currency',
                                  string='Moneda',
                                  default=lambda self: self.env.company.currency_id.id)
    global_credit = fields.Monetary(string = 'Credito Global', required = True, currency_field='currency_id')
    used_credit = fields.Monetary(string = 'Credito Utilizado', compute='_compute_credit', store = True)
    avaiable_credit = fields.Monetary(string = 'Credito disponible',compute='_compute_credit', store = True)
    #Posibilidad de eliminar la relacion y realizar one2many
    partner_ids = fields.Many2many('res.partner', 'res_partner_credit_group_rel', 'credit_group_id', 'partner_id', string='Clientes en el Grupo')

    @api.constrains('code')
    def _check_code(self):
        SEQ = '026'
        for group in self:
            count = self.env['sales.credit.group'].search_count([('code', '=', group.code)])
            #Utilizamos > 1 ya que cuenta el actual / tambien posibilidad de sobreescribir el write
            if count > 1:
                raise ValidationError('Existe un grupo de credito con el mismo codigo')
            if SEQ in group.code:
                raise ValidationError('El codigo del grupo de credito no puede contener la secuencia 026')
    
    @api.depends('global_credit','partner_ids', 'partner_ids.sale_order_ids','partner_ids.sale_order_ids.state', 'partner_ids.invoice_ids','partner_ids.invoice_ids.state')
    def _compute_credit(self):
        for group in self:
            # Ordenes de venta confirmadas sin facturar
            sale_orders = group.partner_ids.mapped('sale_order_ids').filtered(lambda so: so.state == 'sale' and so.invoice_status == 'to invoice')
            # Facturas impagas
            #Al dejar la factura en draft no suma la so en posted pero queda el saldo residual sin sumar en el credito utilizado. se debe contemplar tambien las draft?
            unpaid_invoices = group.partner_ids.mapped('invoice_ids').filtered(lambda inv: inv.state == 'posted' and inv.amount_residual > 0)
            # Sumar los montos convertidos forzado a la moneda de la company
            total_sale_orders = sum(sale_orders.with_company(self.env.company.id).mapped('amount_total'))
            total_unpaid_invoices = sum(unpaid_invoices.with_company(self.env.company.id).mapped('amount_residual'))
            # Calcula el credito utilizado
            used_credit = total_sale_orders + total_unpaid_invoices
            group.used_credit = used_credit
            # Calcula el credito disponible 
            group.avaiable_credit = group.global_credit - used_credit

