# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class stock_move(models.Model):
    _inherit = "stock.move"
    
    def _move_to_update_folowing_product_packing_sequence_change(self, cr, uid, ids, fields=None, arg=None, context=None):
        if type(ids) != type([]):
            ids = [ids]
        return self.pool.get('stock.move').search(cr, uid, [('product_id', 'in', ids)]) or []
    
    def _get_packing_sequence(self, cr, uid, ids, fields, args, context=None):
        result = {}
        for move in self.browse(cr, uid, ids, context=context):
           if move.product_id:
               result[move.id] = int(move.product_id.packing_sequence)
           else:
               result[move.id] = 0
        return result    
    
    _store_packing_sequence = {
        'stock.move': (lambda self, cr, uid, ids, context: ids, ['product_id'], 10),
        'product.product': (_move_to_update_folowing_product_packing_sequence_change, ['packing_sequence'], 10)
    }


    packing_sequence= fields.Integer( string='Packing Sequence',store=_store_packing_sequence,compute=_get_packing_sequence)