from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import logging
_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"
    x_amount_total = fields.Float(string='Total Amount', compute='get_x_total')
    x_tax_total= fields.Float(string='Total tax', compute='get_x_total')
    x_amount_with_tax= fields.Float(string='Total Amount with tax', compute='get_x_total')
    
    @api.onchange('location_id')
    def calculateAvailableQty(self):
        for data in self:
            for lines in data.move_lines:
                location_id = data.location_id.id
                product_id =lines.product_id.id
                query = "select sum(qty) as qty from stock_quant where product_id= "+str(product_id)+" and  location_id = "+str(location_id)+";"
                # _logger.error(query)
                self.env.cr.execute(query)
                data_pharma=self.env.cr.fetchall()
                temp1 = data_pharma[0][0]
                lines.available_qty = temp1 
                # _logger.error(temp1)  
    @api.onchange('move_lines')
    def get_x_total(self):  
        # _logger.error("Inside get total stock picking")
        # self.calculateAvailableQty()
        total_amnt = 0
        total_tax=0
        total_amnt_tax=0
        strquery = "select * from purchase_order_line POL left join purchase_order PO on  PO.id = POL.order_id where PO.name = '"+ str(self.origin)+"'; "
        self.env.cr.execute(strquery)
        data_pharma=self.env.cr.fetchall()
        stockPicking = self.env['purchase.order'].search([('origin', '=', self.origin)])
        for product in self.move_lines:
            productRate= 0
            tax=0
            for data in data_pharma:
                # raise UserError(str(product.product_id.id) + "="+str(data[19]))
                if data[19] == product.product_id.id:
                    productRate=data[3]
                    tax = data[11]
            total_amnt =total_amnt + (product.product_uom_qty * productRate)
            total_tax=total_tax + tax
            # total_amnt + (product.price_unit * product.product_uom_qty )
        total_amnt_tax = total_amnt + total_tax
        self.x_amount_total=total_amnt
        self.x_tax_total=total_tax
        self.x_amount_with_tax=total_amnt_tax
        self.update({
                        'x_amount_total':  total_amnt,
                        'x_tax_total':  total_tax,
                        'x_amount_with_tax':  total_amnt_tax
                        })
        return {'value': {'x_amount_total':  total_amnt, 'x_tax_total':  total_tax, 'x_amount_with_tax':  total_amnt_tax}}
class StockMove(models.Model):
    _inherit="stock.move"
    available_qty  = fields.Float(string="Available forecast")

    @api.onchange('product_id')
    def calculateAvailableQty(self):
        for data in self:
            if data.product_id:
                location_id = data.picking_id.location_id.id
                product_id =data.product_id.id
                query = "select sum(qty) as qty from stock_quant where product_id= "+str(product_id)+" and  location_id = "+str(location_id)+";"
                # _logger.error("from line "+query)
                self.env.cr.execute(query)
                data_pharma=self.env.cr.fetchall()
                temp1 = data_pharma[0][0]
                data.available_qty = temp1 
                # _logger.error(temp1)  

class StockPickingOperation(models.Model):
    _inherit = "stock.pack.operation"
    unitPrice = fields.Float(string='Unit Price', compute='calculateData')
    totalPrice = fields.Float(string='Total Price')
    price_tax = fields.Float(string='Tax Price',default=0)
    
    @api.one
    @api.onchange('picking_id')
    def calculateData(self): 
        # raise UserError("I am here inside stock pack operation price calculkation unit")
        strquery = "select * from purchase_order_line POL left join purchase_order PO on  PO.id = POL.order_id where PO.name = '"+ str(self.picking_id.origin)+"'; " 
        self.env.cr.execute(strquery)
        data_pharma=self.env.cr.fetchall()
        productRate=0
        total_amnt =0
        tax_amnt=0
        for data in data_pharma:
            if data[19] == self.product_id.id:
                productRate=data[3]
                tax_amnt=data[11]
                total_amnt = productRate * float(self.qty_done_uom_ordered)
        self.unitPrice=productRate
        self.totalPrice=total_amnt
        self.price_tax=tax_amnt
        self.update({
                        'unitPrice':  productRate,
                        'totalPrice':  total_amnt,
                        'price_tax':  tax_amnt
                        })
        return {'value': {'unitPrice':  productRate,'totalPrice':  total_amnt, 'price_tax':  tax_amnt}}