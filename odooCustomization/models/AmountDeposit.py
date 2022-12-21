# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
class AmountDeposit(models.Model):
	_name = 'amount.deposit'
	_description = 'Amount Deposit'
	depositer_id = fields.Many2one('res.users', 'Deposited By', required=True,help="Deposited by", default=lambda self: self.env.user)
	deposited_date  =  fields.Date('Depsited date',help="Deposited date", default=datetime.today())
	deposited_amount = fields.Float('Deposited Amount', required=True)
	deposited_to  = fields.Char('Deposited To', required=True,help="Deposited to (Bank or person)")
	depositer_location = fields.Selection([('registration','Registration'),
                                   ('pharmacy','Pharmacy'),
                                   ],string='Depositer Location')

	@api.multi
	def name_get(self):
		result = []
		for record in self:
			record_name = record.depositer_id.name 
			result.append((record.id, record_name))
		return result

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		recs = self.search([('deposited_to', operator, name)] + args, limit=limit)
		return recs.name_get()