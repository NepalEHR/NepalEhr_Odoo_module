# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF, float_is_zero
from datetime import datetime
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('shop_id')
    def _change_shop_loc(self):
        for sale_order in self:
            for sale_order_line in sale_order.order_line:
                sale_order_line.update({
                    'shop_id': sale_order.shop_id
                    })
        

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    today = datetime.today().strftime('%Y-%m-%d')
    shop_id = fields.Many2one('sale.shop', 'Shop')