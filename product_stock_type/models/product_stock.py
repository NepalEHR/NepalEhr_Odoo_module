# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class product_stock_type(models.Model):
    _name = "product.stock_type"
    name= fields.Char(string='Name')
    code= fields.Char(string='Code')


    