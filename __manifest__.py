{
    "name": "Sales Channel Manager",
    "summary": """
        Gestiona diferentes canales de venta para controlar las ventas realizadas como asi la entrega de productos y las facturas asociadas a dichas ventas""",
    "category": "Sales",
    "version": "15.0",
    "author": "Fabian Cerchi - https://github.com/FabiCerchi",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "sale_management",
        "account",
        "sale_stock",
    ],
    "data": [
        'data/sales_channel_data.xml',
        'security/ir.model.access.csv',
        'views/sales_channel_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'views/sales_credit_group_views.xml',
        'views/res_partner_inherit_views.xml',
        'report/credit_group_report.xml'
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

