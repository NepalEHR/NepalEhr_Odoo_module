# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import datetime
import dateutil.parser

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    expired_state = fields.Char(string='Expiration status',default="NOTEXPIRED",compute='_check_the_date')
    # to_expire = fields.Boolean(default=False,compute='_check_the_date')

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
                if life_date >= cur_date and life_date < new_date:
                    rec.expired_state ="TOEXPIRED"
            except:
                rec.expired_state ="NOTEXPIRED"

    # @api.multi
    # def name_get(self):
    #     result = []
    #     count_data =0
    #     # x_available_total = 0
    #     for record in self:
    #         for quant in record.quant_ids:
    #             # if quant.lot_id.id == record.id:
    #             if (quant.location_id.usage == "internal") :
    #                 count_data = count_data + quant.qty
    #                 # x_available_total = quant.x_available_total
    #         record_name = record.name+"["+str(count_data)+"]"
    #         result.append((record.id, record_name))                    
    #     return result