# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'


    @api.multi
    def name_get(self):
        result = []
        for record in self:
            record_name = record.name + '[' + str(record.product_qty)+ ']'
            result.append((record.id, record_name))
        return result