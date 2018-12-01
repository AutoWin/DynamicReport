{
    "name": "Dynamic Report Export",
    "version": "1.0",
    "depends": [],
    "author": "Luong Thanh",
    "category": "Custom",
    "description": """
    This Module can be used to export the XLS reports of the choosen objects using different parameters

    """,
    "depends": [
        'base',
        'stock',
        'sale',
        'purchase',
        'crm',
        'report_xlsx',
    ],
    "data": [
        'views/dynamic_report_view.xml',
    ],
    'js': [],
    'qweb': [],
    'css': [],
    'installable': True,
}