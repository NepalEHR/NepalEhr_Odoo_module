# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import datetime
import dateutil.parser

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    check_date = fields.Boolean(default=False,compute='_check_the_date')

    @api.depends('life_date')
    def _check_the_date(self):
        cur_date = datetime.datetime.now().date()
        new_date = cur_date + datetime.timedelta(days=30)
        for rec in self:
            try:
                life_date = dateutil.parser.parse(rec.life_date).date()
                if life_date < new_date:
                    rec.check_date = True
            except:
                rec.check_date = True
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            record_name = record.name
            result.append((record.id, record_name))
        return result