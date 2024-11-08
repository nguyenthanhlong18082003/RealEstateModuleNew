# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug.urls import url_quote

from odoo import api, models, fields, tools
import logging
_logger = logging.getLogger(__name__)

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    isSoDoNha = fields.Boolean(string="Sổ đỏ", default=False)
    product_id = fields.Many2one("product.template")
    product_id2 = fields.Many2one("product.template")
    @api.model
    def create(self, vals):
        new_record = super(IrAttachment, self).create(vals)
        return new_record
