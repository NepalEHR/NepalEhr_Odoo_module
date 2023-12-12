# -- coding: utf-8 -- 
from odoo import models, fields, api, _
import json
import requests  # Add this line
from odoo.exceptions import UserError
from datetime import datetime 
from time import sleep
import logging


_logger = logging.getLogger(__name__)
class ProductTemplate(models.Model): 
    _name = "product.template"
    _inherit="product.template"

    emergency_price=fields.Float(string="Emergency Price of Service")



class saleOrder(models.Model): 
    _name = "sale.order"
    _inherit="sale.order"

    isEmergencyPrice=fields.Boolean("Emergency price")

class saleorderLine(models.Model):
    _name = "sale.order.line"
    _inherit="sale.order.line"


    @api.onchange('product_id', 'product_id.type','payment_type','isEmergencyPrice','lot_id')
    def _onchange_payment_type(self):   
        if not self.product_id:
            return None

        if not self.payment_type:
            if self.order_id.payment_type:
                self.payment_type = self.order_id.payment_type
                
            else:
                self.payment_type = 'insurance'  # Default to 'insurance' if not set in sale order

        if self.order_id.payment_type == 'cash' and self.payment_type != 'cash':   
            # Raise a warning if trying to change payment type in sale.order.line
            self.payment_type='cash'
            #return  {'warning': {'title':'Warning!!!','message':'You cannot chnage payment type cash.'}}
            return {'warning': {'title': 'Warning!!!', 'message': 'You cannot change payment type to anything other than cash.', 'value': {'payment_type': 'cash'}}}


        if self.payment_type == 'cash':
            if self.product_id.type=='service':
                if self.order_id.isEmergencyPrice:
                    self.price_unit = self.product_id.emergency_price
                else:
                    self.price_unit = self.product_id.list_price
            elif self.product_id.type!='service':
                if self.lot_id:
                    self.price_unit = self.lot_id.sale_price
                else:
                    _logger.error("indoe cash below lot")
                    self.price_unit = self.product_id.list_price
            else:
                self.price_unit = self.product_id.list_price


        elif self.payment_type == 'free':
            self.price_unit = 0
        elif self.payment_type == 'insurance':
            insurance_cost = self.get_insurance_cost(self.product_id)
            if insurance_cost is not None:
                self.price_unit = insurance_cost
            else:
                # Handle the case when insurance_cost is None
                self.price_unit = self.product_id.list_price
                return {'warning': {'title':'Warning!!!','message':'Product not found in mapping. Please contact admin.'}}
        else:
            return {'warning': {'title':'Warning!!!','message':'Payment Type does not exist'}}





