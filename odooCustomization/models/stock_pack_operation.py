from odoo import api, fields, models, _

from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round, float_compare
class PackOperationLot(models.Model):
    _inherit = "stock.pack.operation.lot"
    _description = "Lot/Serial number for pack ops"

    _sql_constraints = [
        ('qty', 'CHECK(qty >= 0.0)', 'Quantity must be greater than or equal to 0.0!'),
        ('uniq_lot_id',  'CHECK(qty >= 0.0)', 'You have already mentioned this lot in another line'),
        ('uniq_lot_name',  'CHECK(qty >= 0.0)', 'You have already mentioned this lot name in another line')
        ]