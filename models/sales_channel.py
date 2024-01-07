# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api


class SalesChannel(models.Model):
    _name = 'sales.channel'
    _description = 'Define un canal para administrar las ventas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string = 'Nombre', required = True, copy = False, tracking = True)
    code = fields.Char(string = 'Codigo', readonly = True, copy = False)
    #Tomo la decision que ambos campos sean requeridos para no indicar alguno por default.
    warehouse_id = fields.Many2one('stock.warehouse', required = True, copy = False)
    journal_id = fields.Many2one('account.journal', required = True, copy = False)
    
    #TODO: Codigo: Una secuencia CH000001 que crezca con cada cliente ingresado