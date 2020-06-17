# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class productTemplate(models.Model):
    _inherit = "product.template"
    stock_type_id= fields.Many2one('product.stock_type',string= 'Stock Type')
    namek= fields.Char(string='Name')
    packing_sequence= fields.Integer(String ='Packing Sequence')
    deliver_in=fields.Selection([('normal','normal'),('iced','Iced'),('warm','Warm'),('cold','Cold'),('iced_n_warm','Warm & Cold')],String ="Website Product Deliver In")
