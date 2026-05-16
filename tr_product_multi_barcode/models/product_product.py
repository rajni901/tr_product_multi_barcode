from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    multi_barcode_ids = fields.One2many(
        'product.barcode',
        'product_id',
        string='Additional Barcodes',
    )

    @api.model
    def _search_by_multi_barcode(self, barcode):
        product = self.search([('barcode', '=', barcode)], limit=1)
        if not product:
            barcode_rec = self.env['product.barcode'].search(
                [('barcode', '=', barcode)], limit=1
            )
            if barcode_rec:
                product = barcode_rec.product_id
        return product


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    multi_barcode_ids = fields.One2many(
        'product.barcode',
        'product_tmpl_id',
        string='Additional Barcodes',
    )
    multi_barcode_count = fields.Integer(
        compute='_compute_multi_barcode_count',
        string='Additional Barcodes',
    )

    def _compute_multi_barcode_count(self):
        for rec in self:
            rec.multi_barcode_count = len(rec.multi_barcode_ids)
