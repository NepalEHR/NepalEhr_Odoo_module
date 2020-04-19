
# -*- coding: utf-8 -*-
{
'name':'NepalEhr Odoo Report',
'description':'Report Section',
'author':'Possible Health',
'website': 'https://www.nepalehr.org/',
'application': True,
   

    'category': 'possibleReport',
    'version': '0.1',

    # any module necessary for this one to work correctly
   'depends':  ['base','board','sale', "mail", "procurement","bahmni_atom_feed", "bahmni_stock" ,"bahmni_account", "account","purchase","stock","stock_account"],


    # always loaded
    'data': [
        'views/reporting_menu.xml',
        'views/report_extended.xml'
  
    ],
}
