import base64
import csv
import io

from odoo import _, fields, models
from odoo.exceptions import UserError


class ImportBarcodeWizard(models.TransientModel):
    _name = 'import.barcode.wizard'
    _description = 'Import Barcodes from CSV'

    csv_file = fields.Binary(string='CSV File', required=True)
    csv_filename = fields.Char(string='Filename')
    result_message = fields.Text(string='Result', readonly=True)

    def _find_product(self, product_ref):
        if not product_ref:
            return False
        Product = self.env['product.template']
        # Search by internal reference
        product = Product.search([('default_code', '=', product_ref)], limit=1)
        if not product:
            # Search by exact name
            product = Product.search([('name', '=', product_ref)], limit=1)
        if not product:
            # Search by name (case-insensitive)
            product = Product.search([('name', 'ilike', product_ref)], limit=1)
        if not product:
            # Search by existing barcode
            product = Product.search([('barcode', '=', product_ref)], limit=1)
        return product

    def action_import(self):
        if not self.csv_file:
            raise UserError(_('Please upload a CSV file.'))

        content = base64.b64decode(self.csv_file).decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))

        imported, skipped = 0, 0
        errors = []

        for i, row in enumerate(reader, start=2):
            product_ref = (row.get('Internal Reference') or '').strip()
            barcode = (row.get('Barcode') or '').strip()
            note = (row.get('Note') or '').strip()

            if not barcode:
                continue

            product = self._find_product(product_ref)

            if not product:
                errors.append(f'Row {i}: Product "{product_ref}" not found. Check the name matches exactly in Odoo.')
                skipped += 1
                continue

            existing = self.env['product.barcode'].search([('barcode', '=', barcode)], limit=1)
            if existing:
                errors.append(f'Row {i}: Barcode "{barcode}" already exists on "{existing.product_tmpl_id.name}".')
                skipped += 1
                continue

            self.env['product.barcode'].create({
                'product_tmpl_id': product.id,
                'barcode': barcode,
                'note': note,
            })
            imported += 1

        msg = f'Imported: {imported} | Skipped: {skipped}'
        if errors:
            msg += '\n\nErrors:\n' + '\n'.join(errors)

        self.result_message = msg
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'import.barcode.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
