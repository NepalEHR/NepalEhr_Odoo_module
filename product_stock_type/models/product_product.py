# -*- coding: utf-8 -*-
from odoo import models,osv, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class products(models.Model):
    _inherit = "product.product"
    # name_en= fields.function(_name_en, method=True, type='char', size=128, string=_('Name EN'), fnct_inv=_name_en_inv)
    # name_cn= fields.function(_name_cn, method=True, type='char', size=128, string=_('Name CN'), fnct_inv=_name_cn_inv)
    # name_sort_en= fields.function(_name_sort_en, method=True, type='char', size=128, store={'product.product': (lambda self, cr, uid, ids, c={}: ids, ['name_en'], 10)}, string=_('Name EN'))
    # name_sort_cn= fields.function(_name_sort_cn, method=True, type='char', size=128, store={'product.product': (lambda self, cr, uid, ids, c={}: ids, ['name_cn'], 10)}, string=_('Name CN'))
