from odoo import models, fields

class Category(models.Model):
    _name = 'category.bds' 

    name = fields.Char(string='Name', required=True)
    