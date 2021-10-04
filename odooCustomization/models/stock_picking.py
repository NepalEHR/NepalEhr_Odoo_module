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
        strquery = "select * from purchase_order_line POL left join purchase_order PO on  PO.id = POL.order_id where PO.name = '"+ str(self.origin)+"'; "
        self.env.cr.execute(strquery)
        data_pharma=self.env.cr.fetchall()
        stockPicking = self.env['purchase.order'].search([('origin', '=', self.origin)])
        for product in self.move_lines:
            productRate= 0
            for data in data_pharma:
                # raise UserError(str(product.product_id.id) + "="+str(data[19]))
                if data[19] == product.product_id.id:
                    productRate=data[3]
            total_amnt =total_amnt + (product.product_uom_qty * productRate)
            # total_amnt + (product.price_unit * product.product_uom_qty )
        self.x_amount_total=total_amnt
        self.update({
                        'x_amount_total':  total_amnt
                        })
        return {'value': {'x_amount_total':  total_amnt}}

class StockPickingOperation(models.Model):
    _inherit = "stock.pack.operation"
    unitPrice = fields.Float(string='Unit Price', compute='calculateData')
    totalPrice = fields.Float(string='Total Price')
    
    @api.one
    @api.onchange('picking_id')
    def calculateData(self): 
        # raise UserError("I am here inside stock pack operation price calculkation unit")
        strquery = "select * from purchase_order_line POL left join purchase_order PO on  PO.id = POL.order_id where PO.name = '"+ str(self.picking_id.origin)+"'; " 
        self.env.cr.execute(strquery)
        data_pharma=self.env.cr.fetchall()
        productRate=0
        total_amnt =0
        for data in data_pharma:
            if data[19] == self.product_id.id:
                productRate=data[3]
                total_amnt = productRate * float(self.qty_done_uom_ordered)
        self.unitPrice=productRate
        self.totalPrice=total_amnt
        self.update({
                        'unitPrice':  productRate,
                        'totalPrice':  total_amnt
                        })
        return {'value': {'unitPrice':  productRate,'totalPrice':  total_amnt}}