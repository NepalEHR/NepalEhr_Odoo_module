# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
class ProductCustomizeTask(models.Model):
	_inherit = 'product.template'
	nehr_id=fields.Char(String="NEHR ID", copy=False)
	orphan_drug = fields.Boolean('Orphan Drug')
	org = fields.Boolean('Org')
	bh = fields.Boolean('BH')
	ch = fields.Boolean('CH')
	x_low_cost_eq = fields.Boolean('MOHP Essesntial Medicine')
	x_govt = fields.Boolean('Government Supply')
	x_formulary = fields.Boolean('Formulary')
	medicine_item = fields.Boolean('Medicine')
	antibiotic = fields.Boolean('Antibiotics')
	lab_item = fields.Boolean('Lab Item')
	physic_medicine = fields.Boolean('Physic Medicine')
	insurance_medicine = fields.Boolean('Insurance Medicine')
	vertical_program = fields.Boolean('Vertical Program')
	dental_item = fields.Boolean('Dental Item')
	medical_item = fields.Boolean('Medical Item')
	other_item = fields.Boolean('Other Item')
	allow_negative_stock = fields.Boolean( string='Allow Negative Stock', help="Allow negative stock levels for the stockable products  attached to this category. The options doesn't apply to products  attached to sub-categories of this category.")

class ProductCategory(models.Model):
    _inherit = "product.category"
    allow_negative_stock = fields.Boolean(  string='Allow Negative Stock',  help="If this option is not active on this product nor on its  product category and that this product is a stockable product,  then the validation of the related stock moves will be blocked if  the stock level becomes negative with the stock move.")
