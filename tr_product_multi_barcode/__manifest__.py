{
    'name': 'Product Multi Barcode',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Products',
    'summary': 'Assign multiple barcodes to a single product with duplicate validation and CSV import',
    'description': """
Product Multi Barcode — by Technical Rajni
==========================================
Assign and manage multiple barcodes for a single product.

Features:
- Multiple barcodes per product variant
- Search by any barcode in Sales, Purchase, Inventory & Invoices
- Duplicate barcode validation
- Bulk barcode import via CSV
- Print barcode labels
- Fast, zero-configuration setup
    """,
    'author': 'Technical Rajni',
    'website': 'https://www.technicalrajni.com',
    'license': 'OPL-1',
    'depends': ['product', 'stock', 'sale', 'purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_barcode_views.xml',
        'views/product_views.xml',
        'wizard/import_barcode_wizard_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 15.00,
    'currency': 'USD',
}
