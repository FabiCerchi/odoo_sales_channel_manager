# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api
import uuid

class SalesChannel(models.Model):
    _name = 'sales.channel'
    _description = 'Define un canal para administrar las ventas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string = 'Nombre', required = True, copy = False, tracking = True, unique = True)
    code = fields.Char(string = 'Codigo', readonly = True, copy = False)
    #Tomo la decision que ambos campos sean requeridos para no indicar alguno por default.
    warehouse_id = fields.Many2one('stock.warehouse', required = True, copy = False)
    journal_id = fields.Many2one('account.journal', required = True, copy = False)
    sequence_id = fields.Many2one('ir.sequence', string='Secuencia', readonly= True, copy=False)

    @api.model
    def create(self, vals):
        if not vals.get('sequence_id'):
            sequence = self.env['ir.sequence'].create({
                'name': f'sale channel seq - {vals["name"]}',
                #Genero un uuid para que el codigo sea unico para cada objeto y pueda incrementar su valor a traves del next_by_code
                'code': str(uuid.uuid4()),
                'prefix': 'CH',
                'padding': 6,
                'number_increment': 1
            })
            vals['sequence_id'] = sequence.id
            vals['code'] = 'CH000000'

        return super(SalesChannel, self).create(vals)
    
