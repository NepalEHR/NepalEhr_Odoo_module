from odoo import api, fields, models, _

from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round, float_compare
from datetime import datetime
class Product(models.Model):
    _inherit = 'product.template'

    qty_low_stock_notify = fields.Integer(string='Notify for Qty Below', default=80,
                                          help='When stock on hand falls below this number, it will be included in the low stock report. Set to -1 to exclude from the report.')

    def send_low_stock_via_email(self):
        header_label_list=["ID", "Name", "Qty On Hand","Qty Incoming","Low Stock Qty"]
        template_obj = self.env['mail.template']
        template_ids = template_obj.search([('name', '=', 'Low Stock Automated Report')])
        template = template_ids[0]
        # template     = template_obj.browse(cr, uid, template_ids)
        if template:
            default_body = template.body_html + "<br> As per the date of "+str(datetime.today().strftime('%Y-%m-%d'))+"</br>"
            custom_body  = """
                <table>
                    <th>%s</th>
                    <th>%s</th>
                    <th style="text-align:center;">%s</th>
                    <th style="text-align:center;">%s</th>
                    <th style="text-align:center;">%s</th>
            """ %(header_label_list[0], header_label_list[1], header_label_list[2], header_label_list[3], header_label_list[4])
            ## Check for low stock products
           
        product_obj = self.env['product.product']
        product_ids = product_obj.search( [('active', '=', True), ('sale_ok', '=', True), ('tracking', '=', 'lot')])
        mydata = "**** STOCK ALERT ****"
        for product in  product_ids:
            qty_available = product.qty_available
            qty_incoming  = product.incoming_qty
            qty_low_stock_notify = product.qty_low_stock_notify
            if qty_available <= qty_low_stock_notify and qty_low_stock_notify >= 0: ## set low_stock_notify = -1 to never be notified
                mydata = str(mydata) + "---"+ str(product.name) + "<=>"+str(qty_available)+ ","
                custom_body += """
                        <tr style="font-size:14px;">
                            <td>%s</td>
                            <td>%s</td>
                            <td style="text-align:center;">%s</td>
                            <td style="text-align:center;">%s</td>
                            <td style="text-align:center;">%s</td>
                        </tr>
                    """ %(product.id, product.name, str(qty_available), str(qty_incoming), str(qty_low_stock_notify))
        custom_body  += "</table>"
        self.env['mail.message'].create({
         'email_from': self.env.user.partner_id.email, # add the sender email
         'author_id': self.env.user.partner_id.id, # add the creator id
         'model': 'mail.channel', # model should be mail.channel
         'type': 'comment',
         'subtype_id': self.env.ref('mail.mt_comment').id, #Leave this as it is
         'body': default_body + custom_body, # here add the message body
         'channel_ids': [(4, 7)], # This is the channel where you want to send the message and all the users of this channel will receive message
         'res_id': 7, # here add the channel you created.
        })
        # self.env.ref('mail.channel_all_employees').id
        template.body_html = default_body
        return True


        