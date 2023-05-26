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

def convert_ad_to_bs(self):
        from datetime import datetime
        convertor=self.date_invoice
        #convert converter date string to date object
        date_obj = datetime.strptime(convertor, '%Y-%m-%d')
        cnvYear=int(date_obj.strftime('%Y'))
        cnvMonth=int(date_obj.strftime('%m'))
        cnvDay=int(date_obj.strftime('%d'))
        convertedDate=self.Adtobs(cnvYear,cnvMonth,cnvDay)
        return str(convertedDate) 


@api.one
def _get_nepali_date(self):
    from datetime import datetime
    iyear = int(date.today().strftime('%Y'))
    imonth = int(date.today().strftime('%m'))
    iday = int(date.today().strftime('%d'))

    convertedDate=self.Adtobs(iyear,imonth,iday) 
    self.update({
                'nepali_date': convertedDate
            })
    self.nepali_date =convertedDate



@api.multi
def print_all_data(self):
    """ Print the invoice and mark it as sent, so that we can see more
        easily the next step of the workflow
    """
    self.ensure_one()
    self.sent = True

    data= self.env['report'].get_action(self, 'bahmni_insurance_odoo.report_invoice_combined')
    return data

def Adtobs(self,engYear,engMonth,engDate):
    
    nepaliMonths = [
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],  #2000
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],  #2001
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 30, 32, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],
                [ 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],  #2071
                [ 31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],  #2072
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31 ],  #2073
                [ 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31 ],
                [ 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30 ],
                [ 31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 32, 31, 32, 30, 31, 30, 30, 29, 30, 30, 30 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 30, 29, 30, 30, 30 ],
                [ 30, 31, 32, 32, 30, 31, 30, 30, 29, 30, 30, 30 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],  #2090
                [ 31, 31, 32, 31, 31, 31, 30, 30, 29, 30, 30, 30 ],
                [ 30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 30, 30, 30, 30 ],
                [ 30, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30 ],
                [ 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30 ],
                [ 31, 31, 32, 31, 31, 31, 29, 30, 29, 30, 29, 31 ],
                [ 31, 31, 32, 31, 31, 31, 30, 29, 29, 30, 30, 30 ]   #2099
            ]

    #engMonth, engDate, engYear = map(int, input("Enter English Month, Date and Year seperated by space: ").split())
    # engMonth=7
    # engDate=18 
    # engYear=2021


    #Define the least possible English date 1944/01/01 Saturday.

    startingEngYear = 1944
    startingEngMonth = 1
    startingEngDay = 1
    dayOfWeek = calendar.SATURDAY  


    #Let's define the equivalent Nepali date 2000/09/17.

    startingNepYear = 2000
    startingNepMonth = 9
    startingNepday = 17


    # Let's calculate the number of days between the two English dates as follows:

    date0=date(engYear,engMonth,engDate)
    date1=date(startingEngYear,startingEngMonth,startingEngDay)
    diff=(date0 - date1).days


    #Initialize required nepali date variables with starting  nepali date
    nepYear = startingNepYear
    nepMonth = startingNepMonth
    nepDay = startingNepday

    #Decreament delta.days until its value becomes zero.
    while diff != 0:

        # Getting total number of days in month nepMonth in a year nepYear
        daysInMonth = nepaliMonths[nepYear - 2000][nepMonth - 1]
        nepDay+=1 # incrementing nepali day

        if(nepDay > daysInMonth):
            nepMonth+=1
            nepDay = 1

        if(nepMonth > 12):
            nepYear+=1
            nepMonth = 1

        dayOfWeek+=1 
        #counting the days in terms of 7 days
        if(dayOfWeek > 7):
            dayOfWeek = 1

        diff-=1	
    # finally we print the converted date
    # print("Your equivalent Nepali date is: %s,%s,%s " %(nepYear, nepMonth, nepDay))
    # convertedBSDATE =str(nepYear) + "/"+str(nepMonth)+"/"+str(nepDay) 
    # raise UserError(convertedBSDATE)
    # return "2077-05-06"
    return str(nepYear) + "/"+str(nepMonth)+"/"+str(nepDay)
