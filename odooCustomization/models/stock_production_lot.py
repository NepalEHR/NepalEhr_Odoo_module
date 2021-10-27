# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import datetime
import dateutil.parser

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    expired_state = fields.Char(string='Expiration status',default="NOTEXPIRED",compute='_check_the_date',store=True)
    # to_expire = fields.Boolean(default=False,compute='_check_the_date')


    def lotCheckFunction(self):
        self.env.cr.execute("update stock_production_lot  set expired_state = 'EXPIRED' where life_date <= now();")
        self.env.cr.execute("update stock_production_lot  set expired_state = 'TOEXPIRED' where life_date > now() and life_date <= (NOW() + INTERVAL '30 DAYS') ;")
        self.env.cr.execute("update stock_production_lot  set expired_state = 'NOTEXPIRED' where  life_date > (NOW() + INTERVAL '30 DAYS') ;")
        return True
    
    pharma_id=23
    store_id=15
    @api.depends('life_date')
    def _check_the_date(self):
        cur_date = datetime.datetime.now().date()
        new_date = cur_date + datetime.timedelta(days=30)
        for rec in self:
            try:
                life_date = dateutil.parser.parse(rec.life_date).date()
                if life_date < cur_date:
                    rec.expired_state ="EXPIRED"
                    return {'value': {'expired_state': 'EXPIRED'}}
                elif life_date >= cur_date and life_date < new_date:
                    rec.expired_state ="TOEXPIRED"
                    return {'value': {'expired_state': 'TOEXPIRED'}}
                else:
                    rec.expired_state ="NOTEXPIRED"
                    return {'value': {'expired_state': 'NOTEXPIRED'}}
            except:
                rec.expired_state ="NOTEXPIRED"
                return {'value': {'expired_state': 'NOTEXPIRED'}}

    @api.multi
    def name_get(self):
        result = []
        count_data =0
        # x_available_total = 0
        for record in self:
            record_name = record.name+"["+str(record.stock_forecast)+"]"
            result.append((record.id, record_name))                    
        return result