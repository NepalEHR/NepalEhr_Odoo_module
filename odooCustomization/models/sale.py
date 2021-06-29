# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF, float_is_zero
from datetime import datetime
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('shop_id')
    def _change_payment_type(self):
        for sale_order in self:
            for sale_order_line in sale_order.order_line:
                sale_order_line.update({
                    'shop_id': sale_order.shop_id
                    })
        

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    today = datetime.today().strftime('%Y-%m-%d')
    shop_id = fields.Many2one('sale.shop', 'Shop')
    # @api.onchange('lot_id')
    # def onchange_lot_id(self):
    #     if self.lot_id:
    #         self.expiry_date = self.lot_id.life_date
    #         if self.env.ref('bahmni_sale.sale_price_basedon_cost_price_markup').value == '1':
    #             self.price_unit = self.lot_id.sale_price if self.lot_id.sale_price > 0.0 else self.price_unit
    #     raise UserError(self.lot_id.expired_state)

    # @api.model
    # def _get_valid_lots(self):
    #     self.lot_id = self.env['stock.production.lot'].search([['life_date', '<', today]])