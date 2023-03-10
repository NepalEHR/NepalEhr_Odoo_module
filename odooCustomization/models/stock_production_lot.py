# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

from datetime import datetime
import dateutil.parser

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    @api.depends('product_id')
    def _get_future_stock_forecast_temp(self):
        """ Gets stock of products for locations
        @return: Dictionary of values
        """
        for lot in self:
            if self._context is None:
                context = {}
            else:
                context = self._context.copy()
            if 'location_id' not in context or context['location_id'] is None:
                locations = self.env['stock.location'].search([('usage', '=', 'internal')])
            elif context.get('search_in_child', False):
                locations = self.env['stock.location'].search([('location_id', 'child_of', context['location_id'])]) or [context['location_id']]
            else:
                context['location_id'] = 15
                locations = self.env['stock.production.lot'].browse(context.get('location_id'))
            if locations:
                self._cr.execute('''select
                        lot_id,
                        sum(qty)
                    from
                        stock_quant
                    where
                        location_id IN %s and lot_id = %s 
                        group by lot_id''',
                        (tuple(locations.ids), lot.id,))
                result = self._cr.dictfetchall()
                if result and result[0]:
                    lot.stock_forecast = result[0].get('sum')

                    product_uom_id = context.get('product_uom', None)
                    if(product_uom_id):
                        product_uom = self.env['product.uom'].browse(product_uom_id)
                        lot.stock_forecast_temp = result[0].get('sum') * product_uom.factor
    expired_state = fields.Char(string='Expiration status',default="NOTEXPIRED",compute='_check_the_date',store=True)
    # to_expire = fields.Boolean(default=False,compute='_check_the_date')
    stock_forecast_temp = fields.Float(string="Available forecast",
                                     compute=_get_future_stock_forecast_temp,
                                     digits=dp.get_precision('Product Unit of Measure'),
                                     help="Future stock forecast quantity of products with this Serial Number available in company warehouses",
                                     store=True
                                     )

    pharma_id=23
    store_id=15
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
            inc = inv_obj.create({
				'product_id': scrapping_item.product_id.id,
				'scrap_qty': scrap_qty,
				'lot_id': scrapping_item.id,
				'location_id':23,
				'scrap_location_id':4,
				'date_expected':datetime.today(),
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