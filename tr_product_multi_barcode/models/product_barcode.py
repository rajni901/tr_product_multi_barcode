from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductBarcode(models.Model):
    _name = 'product.barcode'
    _description = 'Product Multi Barcode'
    _rec_name = 'barcode'

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        ondelete='cascade',
        index=True,
    )
    product_tmpl_id = fields.Many2one(
        related='product_id.product_tmpl_id',
        store=True,
    )
    barcode = fields.Char(
        string='Barcode',
        required=True,
        index=True,
    )
    note = fields.Char(string='Note', help='e.g. Supplier barcode, Old barcode')

    _sql_constraints = [
        ('barcode_uniq', 'unique(barcode)', 'This barcode is already assigned to another product!'),
    ]

    @api.constrains('barcode', 'product_id')
    def _check_duplicate_main_barcode(self):
        for rec in self:
            if self.env['product.product'].search([
                ('barcode', '=', rec.barcode),
                ('id', '!=', rec.product_id.id),
            ], limit=1):
                raise ValidationError(_(
                    'Barcode "%s" is already used as main barcode on another product.', rec.barcode
                ))
