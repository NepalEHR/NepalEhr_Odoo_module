from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import logging
_logger = logging.getLogger(__name__)


class Maintainance(models.Model):
    _inherit = "maintenance.equipment"
    asset_number = fields.Char(string='Asset Number')
    criticality = fields.Selection([('general','General'),
                                   ('important','Important'),
                                   ('very important','Very Important'),
                                   ('critical','Critical'),
                                   ],string='Criticality')
    property_stock_asset= fields.Many2one('stock.location',string=" Location")
    warranty_end_date= fields.Date(string="Warranty End")
    # serial_no = fields.Char('Serial Number',copy=True)

    _sql_constraints = [
        ('serial_no', 'Check(1=1)', "Another asset already exists with this serial number!"),
    ]