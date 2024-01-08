# -*- encoding: utf-8 -*-
from odoo import _, fields, models

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    credit_group_ids = fields.Many2many('sales.credit.group', string='Grupos de Crédito')
