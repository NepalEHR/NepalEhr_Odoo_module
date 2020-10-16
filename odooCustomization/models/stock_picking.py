from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import logging
_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"
    x_amount_total = fields.Float(string='Total Amount', compute='get_x_total')
    y_amount_total = fields.Float(string='Shipped Amount', compute='get_x_total')
    


    @api.onchange('move_lines')
    def get_x_total(self):
        purchase_data = self.env['purchase.order'].search([('name', '=', self.origin)], limit=1) 
        total_amnt=purchase_data.amount_total 
        ship_amnt = 0
        for order in purchase_data.order_line:
            for moves in self.move_lines:
                if moves.product_id == order.product_id:
                    ship_amnt= ship_amnt + order.price_subtotal
        
        self.x_amount_total=total_amnt
        self.y_amount_total=ship_amnt
        self.update({
                        'x_amount_total':  total_amnt,
                        'y_amount_total':  ship_amnt
                        })
        return {'value': {'x_amount_total':  total_amnt,'y_amount_total':  ship_amnt}}