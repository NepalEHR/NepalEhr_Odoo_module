
# -*- coding: utf-8 -*-
{
'name':'Product Categories',
'description':'Add categories to suppliers',
'author':'Possible Health',
'website': 'https://www.nepalehr.org/',
'application': True,
   

    'category': 'Product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','purchase','sale',],

    # always loaded
    'data': [
       
        'views/supplierClassificationView.xml',
        'views/partnerCusotmization.xml'
   
    ],
}
