# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import config, float_compare

import datetime
import dateutil.parser
import json
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    pharma_id=23
    store_id=15
    x_available_total_pharma = fields.Float(string='Pharma Inventory', compute='get_x_available',default=0)
    x_available_total_store = fields.Float(string='Store Inventory', compute='get_x_available',default=0)
    
    @api.onchange('qty')
    def get_x_available(self):  
        total_amnt = 0
        for record in self:
            self.getDataFromDB(record)
    
    def getDataFromDB(self,record):
        temp1=0
        temp2=0
        self.env.cr.execute('select sum(qty) as qty from stock_quant where lot_id = '+str(record.lot_id.id)+' and  location_id = '+str(self.pharma_id)+';')
        data_pharma=self.env.cr.fetchall()
        temp1 = data_pharma[0][0]
        self.env.cr.execute('select sum(qty) as qty from stock_quant where lot_id = '+str(record.lot_id.id)+' and  location_id = '+str(self.store_id)+';')
        data_store=self.env.cr.fetchall()
        temp2 = data_store[0][0]
        record.x_available_total_pharma=temp1
        record.x_available_total_store=temp2
        record.update({
                        'x_available_total_pharma':temp1,
                        'x_available_total_store':temp2
                        })
    
    @api.multi
    @api.constrains('product_id', 'qty')
    def check_negative_qty(self):
        p = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        if (
                config.get('test_enable') and
                not self.env.context.get('test_stock_no_negative')):
            return
        for quant in self:
            if (float_compare(quant.qty, 0, precision_digits=p) == -1 and
                    quant.product_id.type == 'product' and
                    not quant.product_id.allow_negative_stock and
                    not quant.product_id.categ_id.allow_negative_stock):
                msg_add = ''
                if quant.lot_id:
                    msg_add = _(" lot '%s'") % quant.lot_id.name_get()[0][1]
                raise ValidationError(_(
                    "You cannot validate this stock operation because the "
                    "stock level of the product '%s'%s would become negative "
                    "(%s) on the stock location '%s' and negative stock is "
                    "not allowed for this product.") % (
                        quant.product_id.display_name, msg_add, quant.qty,
                        quant.location_id.complete_name))