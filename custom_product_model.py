# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
class ProductCustomizeTask(models.Model):
	_inherit = 'product.template'
	donation = fields.Boolean('Donation', store=True)
	mohpEM = fields.Boolean('MOHP Essesntial Medicine')
	govtSupply = fields.Boolean('Government Supply')
	orphanDrug = fields.Boolean('Orphan Drug')
	dentalItem = fields.Boolean('Dental Item')
