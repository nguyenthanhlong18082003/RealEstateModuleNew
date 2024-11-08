from odoo import http

class MountainController(http.Controller):

    @http.route('/mountain', auth='public', type='http')
    def mountain_check(self):
        return "Hello, world"