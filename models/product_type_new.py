from odoo import models, fields

class ProductType(models.Model):
    _name = 'product.type.new'
    _description = 'Product Type New'

    name = fields.Char(string='Name', required=True)
    image = fields.Binary(string="Image", attachment=True)