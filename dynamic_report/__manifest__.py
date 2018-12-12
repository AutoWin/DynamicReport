{
    "name": "Dynamic Report Export",
    "version": "1.0",
    "depends": [],
    "author": "Luong Thanh",
    "category": "Custom",
    "description": """
        This Module to export all applications to excel
    """,
    "depends": [
        'base',
        'stock',
        'sale',
        'purchase',
        'crm',
        'report_xlsx',
        'web',
    ],
    "data": [
        'views/dynamic_report_view.xml',
        # 'views/report_sale_view.xml',
    ],
    'js': [],
    'qweb': [],
    'css': [],
    'installable': True,
}
