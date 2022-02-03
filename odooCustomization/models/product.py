from odoo import api, fields, models, _

from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round, float_compare
import base64
from datetime import datetime
class Product(models.Model):
    _inherit = 'product.template'

    qty_low_stock_notify = fields.Integer(string='Notify for Qty Below', default=80,
                                          help='When stock on hand falls below this number, it will be included in the low stock report. Set to -1 to exclude from the report.')

    def send_low_stock_via_email(self):
        header_label_list=["ID", "Name", "Qty On Hand","Qty Incoming","Low Stock Qty"]
        product_obj = self.env['product.product']
        product_ids = product_obj.search( [('active', '=', True), ('sale_ok', '=', True), ('tracking', '=', 'lot')])
        stocklowdata ="Sno"+","+header_label_list[0]+ ","+ header_label_list[1]+ ","+header_label_list[2]+ ","+ header_label_list[3]+ ","+ header_label_list[4]+ "\n"
        counter =1
        for product in  product_ids:
            qty_available = product.qty_available
            qty_incoming  = product.incoming_qty
            qty_low_stock_notify = product.qty_low_stock_notify
            if qty_available <= qty_low_stock_notify and qty_low_stock_notify >= 0: ## set low_stock_notify = -1 to never be notified
                stocklowdata = stocklowdata + str(counter)+","+str(product.id)+ ","+ str(product.name.replace(",", "-"))+ ","+ str(qty_available)+ ","+ str(qty_incoming)+ ","+ str(qty_low_stock_notify)+ "\n"      
                counter = counter+1
        now = datetime.now()
        wt = self.env['mail.channel']
        id_needed = wt.search([('name', '=', "low-stock-alert")]).id
        default_body ="<strong>Low Stock Report for "+str(now.strftime("%Y/%m/%d %H:%M:%S"))+"</strong>"
        ATTACHMENT_NAME='Low Stock Report'+str(now.strftime("%Y%m%d_%H_%M_%S"))
        attachment_ids = self.env['ir.attachment'].create({
            'name': 'Low Stock Report',
            'type': 'binary',
            'datas_fname': ATTACHMENT_NAME + '.csv',
            'store_fname': ATTACHMENT_NAME,
            'datas': base64.encodestring(stocklowdata),
            'res_model': 'mail.channel',
            'res_id': id_needed,
            'mimetype': 'application/x-pdf'
        })
        self.env['mail.message'].create({
         'email_from': self.env.user.partner_id.email, # add the sender email
         'author_id': self.env.user.partner_id.id, # add the creator id
         'model': 'mail.channel', # model should be mail.channel
         'type': 'comment',
         'attachment_ids': [(6, 0, [attachment_ids.id])] or None,
         'subtype_id': self.env.ref('mail.mt_comment').id, #Leave this as it is
         'body': default_body, # here add the message body
         'channel_ids': [(4, id_needed)], # This is the channel where you want to send the message and all the users of this channel will receive message
         'res_id': id_needed, # here add the channel you created.
        })

        
