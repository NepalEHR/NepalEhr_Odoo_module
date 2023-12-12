
# -*- coding: utf-8 -*-
{
    'name':'MULTI PRICE',
    'description':'MULTI PRICE',
    'author':'Nepal EHR',
    'website': 'https://www.nepalehr.org/',
    'application': True,
    'category': '',
    'version': '0.1',
    'depends': [
        'base',
        'stock',
        'product',
        'purchase',
        'sale',
        'board', 
        "mail", 
        "procurement",
        "bahmni_atom_feed",
        "bahmni_stock" ,
        "bahmni_account",
        "account",
        "stock_account",
        "maintenance"
    ],
    'data': [
        'views/product_product.xml',
       'views/sale_order.xml',
    ],
}