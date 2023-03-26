# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

import datetime
import dateutil.parser
import logging
_logger = logging.getLogger(__name__)

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    
    def compute_stock_at_once(self):
        # raise UserError("inside compute stock at once")
        _logger.error("inside compute stock at once") 
        stockPicking = self.env['stock.production.lot'].search([('expired_state', '!=', 'EXPIRED')])
        for data in stockPicking:
            scrap_qty=0
            for quant in data.quant_ids:
                if quant.location_id.id == 23:
                    scrap_qty= quant.qty 
            _logger.error(str(scrap_qty)+ "-" + str(data.name))
            data.stock_forecast_temp = scrap_qty
            data.write({
                        'stock_forecast_temp':  scrap_qty, 
                        })
    
    @api.depends('quant_ids')
    def _get_future_stock_forecast_temp(self):
        """ Gets stock of products for locations 
        """
        # for scrapping_item in self: 
        scrap_qty =0
        # self.compute_stock_at_once()
        for data in self:
            for quant in data.quant_ids:
                if quant.location_id.id == 23:
                    scrap_qty= quant.qty 
            _logger.error(scrap_qty)
            data.stock_forecast_temp = scrap_qty 
    expired_state = fields.Char(string='Expiration status',default="NOTEXPIRED",compute='_check_the_date',store=True)
    # to_expire = fields.Boolean(default=False,compute='_check_the_date')
    stock_forecast_temp = fields.Float(string="Available forecast",
                                     compute=_get_future_stock_forecast_temp,  
                                     store=True
                                     )
    active =fields.Boolean(String="Active",default=True)

    pharma_id=23
    store_id=15
    def archive_lot(self):
        for rec in self:
            if not rec.product_qty:
                rec.active = False

    @api.multi
    def action_bulk_archieve(self):
        for scrapping_item in self:
            scrapping_item.active = False
            scrapping_item.write({
                        'active':  False, 
                        })
    @api.multi
    def action_bulk_scrap(self):   
        scrapping_id = ""
        inv_obj = self.env['stock.scrap']
        for scrapping_item in self:
            scrapping_id = scrapping_id + ","+scrapping_item.name
            scrap_qty =0
            for quant in scrapping_item.quant_ids:
                if quant.location_id.id == 23:
                    scrap_qty=scrap_qty+quant.qty
            scrapping_item.stock_forecast_temp = 0
            scrapping_item.write({
                        'stock_forecast_temp':  0, 
                        })
            inc = inv_obj.create({
				'product_id': scrapping_item.product_id.id,
				'scrap_qty': scrap_qty,
				'lot_id': scrapping_item.id,
				'location_id':23,
				'scrap_location_id':4,
				'date_expected':datetime.datetime.today(),
                'product_uom_id': scrapping_item.product_id.uom_id.id
				
				})
        return scrapping_id           
        '''
            Confirm claim for submission
        ''' 
        # raise UserError("Submitting claim in bulk")
    def lotCheckFunction(self):
        self.env.cr.execute("update stock_production_lot  set expired_state = 'EXPIRED' where life_date <= now();")
        self.env.cr.execute("update stock_production_lot  set expired_state = 'TOEXPIRED' where life_date > now() and life_date <= (NOW() + INTERVAL '30 DAYS') ;")
        self.env.cr.execute("update stock_production_lot  set expired_state = 'NOTEXPIRED' where  life_date > (NOW() + INTERVAL '30 DAYS') ;")
        return True
    
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