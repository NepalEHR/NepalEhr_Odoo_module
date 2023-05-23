# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
class PartnerCustomization(models.Model):
    _inherit = 'res.partner'
    is_supplier = fields.Boolean('Is Supplier?')
    supplier_category = fields.Many2one('supplier.classification','Supplier Category', store=True)
    #gender = fields.Selection([('male', 'MALE'), ('female', 'FEMALE'), ('others', 'OTHERS')], string="Select Gender", help="Select Gender" ,required=True)
    #age=fields.Date('Date')
    detail_address=fields.Char('Detail Address')