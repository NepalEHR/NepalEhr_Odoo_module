
# -*- coding: utf-8 -*-
{
'name':'Product Stock Type',
'description': 'Add Product Stock Type',
'author':'Possible Health',
'website': 'https://www.nepalehr.org/',

    'installable': True,
    'auto_install': False,
    'application': False,
   

    'category': 'Product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['product', 'stock'],

    # always loaded
    'data': [
       
       'views/product_view.xml'
   
    ],
}
