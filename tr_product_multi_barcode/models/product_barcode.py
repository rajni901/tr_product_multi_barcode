from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductBarcode(models.Model):
    _name = 'product.barcode'
    _description = 'Product Multi Barcode'
    _rec_name = 'barcode'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True,
        ondelete='cascade',
        index=True,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product Variant',
        ondelete='cascade',
        index=True,
    )
    barcode = fields.Char(string='Barcode', required=True, index=True)
    note = fields.Char(string='Note', help='e.g. Supplier barcode, Old barcode')

    _sql_constraints = [
        ('barcode_uniq', 'unique(barcode)', 'This barcode is already assigned to another product!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('product_tmpl_id'):
                product = self.env['product.product'].browse(vals['product_id'])
                vals['product_tmpl_id'] = product.product_tmpl_id.id
            elif vals.get('product_tmpl_id') and not vals.get('product_id'):
                tmpl = self.env['product.template'].browse(vals['product_tmpl_id'])
                if tmpl.product_variant_ids:
                    vals['product_id'] = tmpl.product_variant_ids[0].id
        return super().create(vals_list)

    @api.constrains('barcode')
    def _check_duplicate_main_barcode(self):
        for rec in self:
            if self.env['product.product'].search([
                ('barcode', '=', rec.barcode),
            ], limit=1):
                raise ValidationError(_(
                    'Barcode "%s" is already used as main barcode on a product.', rec.barcode
                ))
