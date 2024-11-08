from odoo import models, fields, api

class ContactResPartner(models.Model):
    _inherit = 'res.partner'

    number_zalo = fields.Char(string="Zalo")
    product_for_sale_ids = fields.One2many('product.template', 'saler_id', string="Product for sale")