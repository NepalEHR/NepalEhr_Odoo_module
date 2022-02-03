# -*- coding: utf-8 -*-
from odoo import models, fields, api
class SupplierClassification(models.Model):
	_name = 'supplier.classification'
	_description = 'Supplier Category'
	category_name = fields.Char('Category', required=True)
	is_active  =  fields.Boolean('Is Active?')
	@api.multi
	def name_get(self):
		result = []
		for record in self:
			record_name = record.category_name 
			result.append((record.id, record_name))
		return result

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		recs = self.search([('category_name', operator, name)] + args, limit=limit)
		return recs.name_get()