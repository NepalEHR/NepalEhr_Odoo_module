# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class product_stock_type(models.Model):
    _name = "product.stock_type"
    name= fields.Char(string='Name')
    code= fields.Char(string='Code')

class product_template(models.Model):
    _inherit = "product.template"
    stock_type_id= fields.many2one('product.stock_type', 'Stock Type')
    name= fields.Char(string='Name')

class product_product(models.Model):
    _inherit = "product.product"
    packing_sequence= fields.Integer('Packing Sequence')
    deliver_in=fields.selection([('normal','normal'),('iced','Iced'),('warm','Warm'),('cold','Cold'),('iced_n_warm','Warm & Cold')],help="Website Product Deliver In",required=True)
    # name_en= fields.function(_name_en, method=True, type='char', size=128, string=_('Name EN'), fnct_inv=_name_en_inv)
    # name_cn= fields.function(_name_cn, method=True, type='char', size=128, string=_('Name CN'), fnct_inv=_name_cn_inv)
    # name_sort_en= fields.function(_name_sort_en, method=True, type='char', size=128, store={'product.product': (lambda self, cr, uid, ids, c={}: ids, ['name_en'], 10)}, string=_('Name EN'))
    # name_sort_cn= fields.function(_name_sort_cn, method=True, type='char', size=128, store={'product.product': (lambda self, cr, uid, ids, c={}: ids, ['name_cn'], 10)}, string=_('Name CN'))

class stock_move(models.Model):
    _inherit = "stock.move"
    packing_sequence= fields.Integer( string='Packing Sequence')
    
    # def _move_to_update_folowing_product_packing_sequence_change(self, cr, uid, ids, fields=None, arg=None, context=None):
    #     if type(ids) != type([]):
    #         ids = [ids]
    #     return self.pool.get('stock.move').search(cr, uid, [('product_id', 'in', ids)]) or []
    
    # def _get_packing_sequence(self, cr, uid, ids, fields, args, context=None):
    #     result = {}
    #     for move in self.browse(cr, uid, ids, context=context):
    #        if move.product_id:
    #            result[move.id] = int(move.product_id.packing_sequence)
    #        else:
    #            result[move.id] = 0
    #     return result    
    
    # _store_packing_sequence = {
    #     'stock.move': (lambda self, cr, uid, ids, context: ids, ['product_id'], 10),
    #     'product.product': (_move_to_update_folowing_product_packing_sequence_change, ['packing_sequence'], 10)
    # }
    # compute=_get_packing_sequence,
    # , store=_store_packing_sequence

    