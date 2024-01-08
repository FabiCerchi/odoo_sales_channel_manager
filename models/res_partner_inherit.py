# -*- encoding: utf-8 -*-
from odoo import _, fields, models, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    credit_control = fields.Selection([('yes', 'Si'),
                                       ('no', 'No')],
                                       string='Control de Credito',
                                       default='no')
    #TODO: Posibilidad de eliminar la relacion inversa
    credit_group_ids = fields.Many2many('sales.credit.group', string='Grupos de Crédito')
