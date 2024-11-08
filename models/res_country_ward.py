from odoo import models, fields

class ResCountryWard(models.Model):
    _name = 'res.country.ward_new'
    _description = 'Ward'

    name = fields.Char(string='Ward Name', required=True)
    district_id = fields.Many2one('res.country.district_new', string='District', required=True)
    code = fields.Char(string='Ward Code')
