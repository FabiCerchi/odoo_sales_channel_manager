# -*- coding: utf-8 -*-
import logging
import odoo
from odoo import http
from odoo.http import request

CORS = '*'


class SalesCreditGroupController(http.Controller):
    
    @http.route('/pgk-api/credit', type="json", auth='none', cors=CORS, method=['POST'])
    def create_credit_group(self, grupo_creditos = [], **kw):
        '''
        Proposito: Crear / actualizar grupos de creditos a traves de un endpoint
        
        '''
        try:
            if not grupo_creditos:
                return {
                    'status': 400,
                    'message': 'Json invalido para grupos de creditos'
                }
                
            for credit_group in grupo_creditos:
                #antes de realizar la creacion - actualizacion validamos que exista el canal 
                #El primer canal con dicho codigo lo asignara, Pueden existir varios canales con mismo codigo, ya que se incrementa el mismo se incrementa secuencialmente.
                channel = request.env['sales.channel'].sudo().search([('code','=',credit_group['canal'])], limit=1)
                if not channel:
                    return {
                            'status': 400,
                            'message': f"No se encontró el canal {credit_group['canal']}"
                        }
                        
                group = request.env['sales.credit.group'].sudo().search([('code','=',credit_group['codigo'])], limit=1)

                if not group:
                #Creacion del grupo de credito
                    try:
                        group_id = group.sudo().create({
                            'name': credit_group['name'],
                            'code': credit_group['codigo'],
                            'sale_channel_id': channel.id,
                            'global_credit': credit_group['credito_global']
                        })
                    except Exception as e:
                        return {'status': "Error", 'message': str(e)}
                else:
                #Actualizacion del grupo de credito:
                    try:
                        group_id = group.sudo().write({
                            'name': credit_group['name'],
                            'sale_channel_id': channel.id,
                            'global_credit': credit_group['credito_global']
                        })
                    except Exception as e:
                        return {'status': "Error", 'message': str(e)}

            return {
                'status': 200,
                'message': 'OK'
            }                
                
        except Exception as e:
            return {'status': "Error", 'message': str(e)}
    