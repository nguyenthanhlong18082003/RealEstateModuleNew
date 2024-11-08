from odoo import models, fields, api

class ContactResUser(models.Model):
    _inherit = 'res.users'

    number_zalo = fields.Char(string="Zalo")