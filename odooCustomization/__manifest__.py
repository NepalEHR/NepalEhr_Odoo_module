
# -*- coding: utf-8 -*-
{
    'name':'Nyaya Customization',
    'description':'Customization as per Nepal Electronic Health Record',
    'author':'Possible Health',
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
        'views/stock_picking.xml',
        'report/delivery_slip.xml',
        'views/product_categories.xml',
        'views/supplierClassificationView.xml',
        'views/partnerCusotmization.xml',
        'views/reporting_menu.xml',
        'views/report_extended.xml',
        'views/maintainance_view.xml',
        'views/procurememt_view.xml',
        'views/stock_production_lot.xml' ,
        'views/stock_quant.xml'   ,
        'views/kpi_report.xml'       ,
        'views/sale_order_view.xml'    ,
        'views/account_invoice_report_view_custom.xml'  ,
        'views/sales_purchase_report_modification.xml'
    ],
}
