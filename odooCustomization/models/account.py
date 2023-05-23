from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
import datetime 
import time
import calendar
import logging
import math
_logger = logging.getLogger(__name__)


import base64
class account_invoice(models.Model):
    _inherit = 'account.invoice'

    def calculate_age(self,dob_str):
        #if not isinstance(dob_str, str):
            #return "-"
        # try:
        #     dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
        # except ValueError:
        #     raise ValueError("dob_str must be in the format 'YYYY-MM-DD'")
        if not dob_str:
            return ""
        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
        now=datetime.datetime.now()
        age_in_days = (now - dob).days
        age_in_years = age_in_days / 365.25
        age_ceiling = math.ceil(age_in_years)
        age_int=int(age_ceiling)
        return str(age_int)
    
    def short_address(self,full_address):
        if not full_address:
            return ""
        strr = full_address.split(',')
        cityVillage = strr[0]
        address1 = strr[1]
        district= strr[2]
        address = ''.join(cityVillage +"-"+address1 +","+ district)
        return address


