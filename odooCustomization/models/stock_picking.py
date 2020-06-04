from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import logging
_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"
    x_amount_total = fields.Float(string='Total Amount', compute='get_x_total')
    


    @api.onchange('move_lines')
    def get_x_total(self):  
        _logger.info("Inside get total stock picking")
        total_amnt = 0
        for product in self.move_lines:
            total_amnt = total_amnt + (product.price_unit * product.product_uom_qty )
        self.x_amount_total= total_amnt
        self.update({
                        'x_amount_total':  total_amnt
                        })
        return {'value': {'x_amount_total':  total_amnt}}