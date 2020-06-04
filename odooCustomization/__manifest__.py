
# -*- coding: utf-8 -*-
{
'name':'Odoo Customization',
'description':'Customization as per Nepal Electronic Health Record',
'author':'Possible Health',
'website': 'https://www.nepalehr.org/',
'application': True,
   

    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
       
       'views/stock_picking.xml',
       'report/delivery_slip.xml',
        'views/stock_transfer.xml'
    ],
}
